from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.routes.candidate import (
    router as candidate_router,
)
from app.api.routes.dashboard import (
    router as dashboard_router,
)
from app.api.routes.jobs import (
    router as jobs_router,
)
from app.api.routes.resume import (
    router as resume_router,
)

from app.api.routes.matching import router as matching_router


app = FastAPI(
    title="AI Recruitment Platform",
    version="1.0.0",
)


# ----------------------------------------------------------------------
# Routers
# ----------------------------------------------------------------------

app.include_router(matching_router, prefix="/api/v1")

app.include_router(
    dashboard_router,
    prefix="/api/v1",
)

app.include_router(
    jobs_router,
    prefix="/api/v1",
)

app.include_router(
    resume_router,
    prefix="/api/v1",
)

app.include_router(
    candidate_router,
    prefix="/api/v1",
)


# ----------------------------------------------------------------------
# Health Check
# ----------------------------------------------------------------------


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-recruitment-platform",
    }


# ----------------------------------------------------------------------
# Custom OpenAPI
# ----------------------------------------------------------------------


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    components = (
        schema
        .get("components", {})
        .get("schemas", {})
    )

    for component in components.values():
        properties = component.get(
            "properties",
            {},
        )

        for prop in properties.values():

            if (
                prop.get("contentMediaType")
                == "application/octet-stream"
            ):
                prop.pop(
                    "contentMediaType",
                    None,
                )

                prop["format"] = "binary"

            items = prop.get("items")

            if isinstance(items, dict):

                if (
                    items.get("contentMediaType")
                    == "application/octet-stream"
                ):
                    items.pop(
                        "contentMediaType",
                        None,
                    )

                    items["format"] = "binary"

    app.openapi_schema = schema

    return app.openapi_schema


app.openapi = custom_openapi