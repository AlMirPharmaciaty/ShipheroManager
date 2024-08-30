from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.config.settings import Settings
from src.config.database import init_db
from src.api import routes, tags_metadata


def my_app():
    """
    Loading environment variables
    and initializing the app
    """
    settings = Settings()
    init_db()

    app = FastAPI(title=settings.TITLE,
                  openapi_tags=tags_metadata,
                  docs_url='/')
    app.mount("/static", StaticFiles(directory="src/static"), name="static")
    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"],)
    app.include_router(routes)

    return app
