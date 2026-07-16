"""
Aplicacion FastAPI - Sistema de Votaciones.
Ejecutar con:
  uvicorn src.utils.app:app --reload --host 127.0.0.1 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.config import get_settings
from src.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from src.core.exceptions import AppException
from src.database.config import create_tables
from src.endpoints import Candidate, Vote, Voter

# Importar modelos para que Base.metadata los conozca
import src.entities.Voter  # noqa: F401
import src.entities.Candidate  # noqa: F401
import src.entities.Vote  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="API Sistema de Votaciones",
    description="API RESTful para gestionar votantes, candidatos y votos",
    version="1.0.0",
    lifespan=lifespan,
)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar handlers globales de errores
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Routers de endpoints
app.include_router(Voter.router)
app.include_router(Candidate.router)
app.include_router(Vote.router)


@app.get("/")
def inicio():
    return {
        "success": True,
        "data": {"mensaje": "API Sistema de Votaciones", "docs": "/docs"},
    }
