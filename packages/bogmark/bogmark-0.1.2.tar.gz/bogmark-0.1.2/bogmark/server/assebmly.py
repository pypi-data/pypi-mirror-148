import itertools
import os
from typing import Any, Union

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import PlainTextResponse
from starlette_prometheus import metrics

from bogmark.server.middlewares import headers, logs, prometheus
from bogmark.logger import get_logger

from .dependecies import check_headers
from .errors import register_errors
from .responses import ErrorSchemaResponse

logger = get_logger(__name__)


def disable_logging():
    def decorator(func):
        func.disable_logging = True
        return func

    return decorator


@disable_logging()
def basic_ping_endpoint():
    return PlainTextResponse("pong")


@disable_logging()
def healthz_endpoint():
    return {"temperature": 36.6}


@disable_logging()
def metrics_endpoint(request: Request):
    return metrics(request)


def set_error_response_openapi(description: str = ""):
    return {"description": description, "model": ErrorSchemaResponse}


responses = {
    status.HTTP_400_BAD_REQUEST: set_error_response_openapi(),
    status.HTTP_401_UNAUTHORIZED: set_error_response_openapi(),
    status.HTTP_404_NOT_FOUND: set_error_response_openapi(),
    status.HTTP_403_FORBIDDEN: set_error_response_openapi(),
    status.HTTP_500_INTERNAL_SERVER_ERROR: set_error_response_openapi(),
}


def set_allowed_responses(codes: Union[list[int], dict[int, str]]) -> dict[str, Any]:
    if isinstance(codes, list):
        codes_set = set(codes)
        codes_set.add(500)  # because no one writes perfect code 👿
        res = {key: value for key, value in responses.items() if key in codes}
    elif isinstance(codes, dict):
        codes[500] = ""
        res = {key: set_error_response_openapi(codes[key]) for key in responses if key in codes}
    else:
        raise ValueError("codes should be `list` or `dict`")

    return res


def register_routers(
    routers=(), on_startup=(), on_shutdown=(), openapi_url="/openapi.json", ping_endpoint=None, version: str = "0.1.0"
):
    if ping_endpoint is None:
        ping_endpoint = basic_ping_endpoint

    app = FastAPI(on_startup=on_startup, on_shutdown=on_shutdown, openapi_url=openapi_url, version=version)

    title = os.getenv("FASTAPI_TITLE", "FastAPI")
    description = os.getenv("FASTAPI_DESCRIPTION", "")
    app.title = title
    app.description = description

    register_errors(app)
    headers.register(app)
    logs.register(app)
    prometheus.register(app)

    for router_data in itertools.chain(*routers):
        for route in router_data["router"].routes:
            if not route.responses:
                route.responses = responses
        app.include_router(
            router=router_data["router"],
            tags=router_data["tags"],
            prefix=router_data["prefix"],
            dependencies=[Depends(d) for d in router_data["dependencies"]],
        )
    app.add_api_route(path="/readiness", endpoint=ping_endpoint, tags=["Probes"], include_in_schema=False)
    app.add_api_route(path="/liveness", endpoint=healthz_endpoint, tags=["Probes"], include_in_schema=False)
    app.add_api_route(path="/metrics", endpoint=metrics_endpoint, tags=["Probes"], include_in_schema=False)
    return app


def compile_routers(routers, root_prefix: str = "", dependencies=None):
    compiled_routers = []
    common_dependencies = dependencies or []
    for router in routers:
        r = {**router}

        dependencies = r.get("dependencies", [])
        dependencies.extend(common_dependencies)

        if not r.get("disable_check_headers", False):
            dependencies.append(check_headers)

        r["prefix"] = root_prefix + r["prefix"]
        r["tags"] = [f"{root_prefix.lstrip('/')} {tag}" for tag in r["tags"] or []]
        r["dependencies"] = dependencies
        compiled_routers.append(r)

    return compiled_routers
