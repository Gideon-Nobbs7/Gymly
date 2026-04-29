import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from app.config.database_config import Base
from app.core.types import UUID


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        UUID(),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
