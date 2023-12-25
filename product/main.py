import os
import asyncio
import signal
import click
import uvicorn
from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging.config
import logging

from api import router

from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    ResponseLogMiddleware,
)
from settings import APP_PORT, APP_HOST


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
        ),
        Middleware(ResponseLogMiddleware, logger=logging.getLogger("ppm-request")),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Product Service",
        description="Product Service",
        version="0.0.1",
        docs_url="/docs",
        redoc_url="/redocs",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},  # -1,0,1
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


#
app = create_app()


@app.on_event("startup")
async def handle_start_up_sequence():
    print("Startup function is called")


@app.on_event("shutdown")  # new
async def app_shutdown():
    print("Shutdown function is called")


if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(
        signal.SIGQUIT, lambda _: asyncio.create_task(app_shutdown())
    )


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=True,
)
def main(env: str, debug: bool):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=True if env != "production" else False,
        workers=1,
        debug=debug,
    )


if __name__ == "__main__":
    main()
