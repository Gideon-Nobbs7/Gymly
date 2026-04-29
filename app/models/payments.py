
from sqlalchemy import (UUID, Column, Date, Enum, ForeignKey, Numeric,
                        String)
from sqlalchemy.orm import relationship

from app.core.core import PaymentType
from app.models.base_model import BaseModel


class Payment(BaseModel):
    __tablename__ = "payments"
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    amount = Column(Numeric(precision=10, scale=2), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    payment_date = Column(Date, nullable=False)
    recorded_by = Column(String, nullable=True)

    member = relationship("Member", back_populates="payments")
