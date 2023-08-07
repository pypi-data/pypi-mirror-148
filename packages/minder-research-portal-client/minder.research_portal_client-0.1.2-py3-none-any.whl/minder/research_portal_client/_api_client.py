import asyncio
import datetime
import logging
from types import TracebackType
import aiohttp
import re
import warnings
from typing import Any, Dict, Optional, Type, TypeVar, Union, final
import yarl
from minder.research_portal_client import Configuration
import minder.research_portal_client.models as models
import traceback
import sys


_T = TypeVar("_T")
logger = logging.getLogger(__name__)


def _with_config(target):
    def api_call(self, *args, **kwargs):
        if self.closed:
            raise RuntimeError("API client is closed")

        self._session.headers.update({"Authorization": f"Bearer {self.configuration.access_token}"})

        func = target(self)

        url: Union[str, yarl.URL] = args[0]

        if isinstance(url, str):
            url = yarl.URL(url)

        url = url.with_path(f"{self.configuration.path_prefix}{url.path}")

        args = list(args)
        args[0] = url

        return func(*tuple(args), **kwargs)

    return api_call


@final
class ApiClient(object):
    PRIMITIVE_TYPES = (float, bool, bytes, str, int)
    NATIVE_TYPES_MAPPING = {
        "int": int,
        "long": int,
        "float": float,
        "str": str,
        "bool": bool,
        "date": datetime.date,
        "datetime": datetime.datetime,
        "object": object,
    }

    def __init__(self, configuration: Configuration = None, *, loop: asyncio.AbstractEventLoop = None):
        self._loop = aiohttp.helpers.get_running_loop(loop)

        if self._loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        if configuration is None:
            configuration = Configuration()
        self.configuration = configuration

        headers = {}
        if configuration.debug:
            headers["X-Azure-DebugInfo"] = "1"

        async def on_request_start(_, trace_config_ctx, params: aiohttp.TraceRequestStartParams):
            trace_config_ctx.start = asyncio.get_event_loop().time()

        async def on_request_end(_, trace_config_ctx, params: aiohttp.TraceRequestEndParams):
            elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
            logger.debug(
                "%s %s %d %.3f ms - %d",
                params.method,
                params.url,
                params.response.status,
                elapsed,
                params.response.content_length,
            )

        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(on_request_start)
        trace_config.on_request_end.append(on_request_end)

        self._session = aiohttp.ClientSession(
            self.configuration.base_url,
            loop=self._loop,
            connector=aiohttp.TCPConnector(ssl=self.configuration.ssl),
            headers=headers,
            trace_configs=[trace_config],
        )

    def __del__(self, _warnings: Any = warnings) -> None:
        if not self.closed:
            kwargs: Dict = {}
            _warnings.warn(f"Unclosed  API client {self!r}", ResourceWarning, **kwargs)
            context = {"api_client": self, "message": "Unclosed API client"}
            if self._loop.get_debug():
                context["source_traceback"] = self._source_traceback
            self._loop.call_exception_handler(context)

    def __enter__(self) -> None:
        raise TypeError("Use async with instead")

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self):
        if not self.closed:
            await self._session.close()
            self._session = None

    @property
    def closed(self):
        return self._session is None or self._session.closed

    @_with_config
    def head(self):
        return self._session.head

    @_with_config
    def get(self):
        return self._session.get

    @_with_config
    def post(self):
        return self._session.post

    @_with_config
    def put(self):
        return self._session.put

    @_with_config
    def delete(self):
        return self._session.delete

    @property
    def info(self):
        from minder.research_portal_client.api import InfoApi

        return InfoApi(self)

    @property
    def export(self):
        from minder.research_portal_client.api import ExportApi

        return ExportApi(self)

    @property
    def download(self):
        from minder.research_portal_client.api import DownloadApi

        return DownloadApi(self)

    @property
    def reports(self):
        from minder.research_portal_client.api import ReportsApi

        return ReportsApi(self)

    async def deserialize(self, response: aiohttp.ClientResponse, response_type: Union[Type[_T], str]) -> _T:
        json = await response.json()

        try:
            return self.__deserialize(json, response_type)

        except ValueError:
            return json

    def __deserialize(self, data, klass: "Union[Type, str]"):
        if data is None:
            return None

        if isinstance(klass, str):
            if klass.startswith("list["):
                match = re.match(r"list\[(.*)\]", klass)
                sub_kls = match.group(1) if match is not None else list
                return [self.__deserialize(sub_data, sub_kls) for sub_data in data]

            if klass.startswith("dict("):
                match = re.match(r"dict\(([^,]*), (.*)\)", klass)
                sub_kls = match.group(2) if match is not None else dict
                return {k: self.__deserialize(v, sub_kls) for k, v in data.items()}

            if klass in self.NATIVE_TYPES_MAPPING:
                klass = self.NATIVE_TYPES_MAPPING[klass]
            else:
                klass = getattr(models, klass)

        if klass in self.PRIMITIVE_TYPES:
            return self.__deserialize_primitive(data, klass)

        if klass == object:
            return data

        if klass == datetime.date:
            return self.__deserialize_date(data)

        if klass == datetime.datetime:
            return self.__deserialize_datetime(data)

        return self.__deserialize_model(data, klass)

    def __deserialize_primitive(self, data, klass):
        try:
            return klass(data)
        except UnicodeEncodeError:
            return str(data)
        except TypeError:
            return data

    def __deserialize_date(self, string):
        try:
            from dateutil.parser import parse

            return parse(string).date()
        except ImportError:
            return string
        except ValueError:
            raise ApiException(status=0, reason="Failed to parse `{0}` as date object".format(string))

    def __deserialize_datetime(self, string):
        try:
            from dateutil.parser import parse

            return parse(string)
        except ImportError:
            return string
        except ValueError:
            raise ApiException(status=0, reason=("Failed to parse `{0}` as datetime object".format(string)))

    def __hasattr(self, object, name):
        return name in object.__dict__ or name in object.__class__.__dict__

    def __deserialize_model(self, data, klass):
        if not klass.prop_types and not self.__hasattr(klass, "get_real_child_model"):
            return data

        kwargs = {}
        if klass.prop_types is not None:
            for attr, attr_type in klass.prop_types.items():
                if data is not None and klass.attribute_map[attr] in data and isinstance(data, (list, dict)):
                    value = data[klass.attribute_map[attr]]
                    kwargs[attr] = self.__deserialize(value, attr_type)

        instance = klass(**kwargs)

        if isinstance(instance, dict) and klass.prop_types is not None and isinstance(data, dict):
            for key, value in data.items():
                if key not in klass.prop_types:
                    instance[key] = value
        if self.__hasattr(instance, "get_real_child_model"):
            klass_name = instance.get_real_child_model(data)
            if klass_name:
                instance = self.__deserialize(data, klass_name)
        return instance


class ApiException(Exception):
    def __init__(
        self,
        status: int = None,
        reason: str = None,
        message: str = None,
        http_resp: aiohttp.ClientResponse = None,
        content: str = None,
    ):
        self.message = message

        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.headers = http_resp.headers

            self.body = content
            http_resp.release()
        else:
            self.status = status or 0
            self.reason = reason

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n" "Reason: {1}\n".format(self.status, self.reason)

        if self.message:
            error_message += "Message: {0}\n".format(self.message)

        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
