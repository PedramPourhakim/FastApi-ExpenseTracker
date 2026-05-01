from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi_swagger import patch_fastapi
from contextlib import asynccontextmanager
from expenses.routes import router as expenses_routes
from people.routes import router as people_routes
from users.routes import router as users_routes
from core.i18n import load_translations
from fastapi.exceptions import RequestValidationError
from utils.exception_handler import ValidationExceptionHandler, HttpExceptionHandler

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from core.config import settings
import sentry_sdk

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0
)
# pybabel compile -d locales

SUPPORTED_LANGUAGES = {"en", "fa"}
DEFAULT_LANGUAGE = "en"

redis = aioredis.from_url(settings.REDIS_URL)
cache_backend = RedisBackend(redis)
FastAPICache.init(cache_backend,prefix="fastapi-cache")


tags_metadata = [
    {
        "name": "expenses",
        "description": "Operations related to expense management",
        "externalDocs": {
            "description": "More about expenses",
            "url": "https://fastapi.tiangolo.com/api/#expenses",
        },
    },
    {
        "name": "users",
        "description": "Operations related to users management",
        "externalDocs": {
            "description": "More about users",
            "url": "https://fastapi.tiangolo.com/api/#users",
        },
    },
    {
        "name": "people",
        "description": "Operations related to people management",
        "externalDocs": {
            "description": "More about people",
            "url": "https://fastapi.tiangolo.com/api/#people",
        },
    },
]


@asynccontextmanager
async def lifespan(app_arg: FastAPI):
    load_translations()
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(
    title="Expense Tracker Application",
    description="This is a section for description",
    version="0.0.1",
    summary="Some dummy summary",
    terms_of_service="http://example.com",
    contact={
        "name": "Pedram Pourhakim",
        "url": "https://www.pedram.com/",
        "email": "pedrampourhakim1999@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=None,
    swagger_ui_oauth2_redirect_url=None,
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)
patch_fastapi(app, docs_url="/swagger")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return HttpExceptionHandler().handle_exception(exc)


@app.exception_handler(RequestValidationError)
async def http_validation_exception_handler(request, exc):
    return ValidationExceptionHandler().handle_exception(exc)


app.include_router(people_routes, prefix="/api/v1")
app.include_router(expenses_routes, prefix="/api/v1")
app.include_router(users_routes, prefix="/api/v1")

@app.get("/is-ready",status_code=200)
async def readiness():
    return JSONResponse(content="OK")

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
# @app.middleware("http")
# async def dispatch(request: Request, call_next):
#     lang = request.query_params.get("lang")
#     if not lang:
#         accept_lang = request.headers.get("accept-language")
#         if accept_lang:
#             lang = accept_lang.split(",")[0].split("-")[0]
#     if lang not in SUPPORTED_LANGUAGES:
#         lang = DEFAULT_LANGUAGE
#     request.state.lang = lang
#     response = await call_next(request)
#     return response
