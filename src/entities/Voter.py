"""Modelo ORM de Votante (Voter)."""

import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class Voter(Base):
    __tablename__ = "voters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    has_voted = Column(Boolean, default=False, nullable=False)
