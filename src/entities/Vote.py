"""Modelo ORM de Voto (Vote)."""

import uuid

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    voter_id = Column(UUID(as_uuid=True), ForeignKey("voters.id"), nullable=False)
    candidate_id = Column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    voter = relationship("Voter")
    candidate = relationship("Candidate")
