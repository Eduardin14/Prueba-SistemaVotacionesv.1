"""
Configuracion de base de datos.
- Produccion/CI: usa DATABASE_URL (PostgreSQL/MySQL).
- Desarrollo local: usa SQLite si DATABASE_URL no esta definida.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    db_path = Path(__file__).resolve().parents[2] / "dev.db"
    DATABASE_URL = f"sqlite:///{db_path.as_posix()}"

_engine_kwargs = {
    "echo": False,  # Cambiar a True para ver consultas SQL
    "pool_pre_ping": True,
}

if DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, **_engine_kwargs)

# Crear la sesion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """Generador de sesiones de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crear todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)
