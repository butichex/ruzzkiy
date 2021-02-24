from fastapi import FastAPI, HTTPException, Depends
from starlette import status
from starlette.requests import Request
import settings
import uvicorn
from routers import api_router

docs_kwargs = {}  # noqa: pylint=invalid-name
if settings.ENVIRONMENT == 'production':
    docs_kwargs = dict(docs_url=None, redoc_url=None)  # noqa: pylint=invalid-name

app = FastAPI(**docs_kwargs)  # noqa: pylint=invalid-name
app.include_router(api_router)
uvicorn.run(app)
