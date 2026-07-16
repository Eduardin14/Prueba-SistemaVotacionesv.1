"""Modelo ORM de Candidato (Candidate)."""

import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    votes = Column(Integer, default=0, nullable=False)
