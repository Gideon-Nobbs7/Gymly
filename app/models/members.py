import enum

from sqlalchemy import Boolean, Column, Date, Enum, String
from sqlalchemy.orm import relationship

from app.core.core import MembershipStatus, PlanType
from app.models.base_model import BaseModel


class Member(BaseModel):
    __tablename__ = "members"

    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False, unique=True)
    date_joined = Column(Date, nullable=True)
    plan_type = Column(Enum(PlanType), nullable=False)
    status = Column(
        Enum(MembershipStatus), nullable=False, default=MembershipStatus.active
    )
    expiry_date = Column(Date, nullable=True)
    lifetime_registered = Column(Boolean, default=False)
    lifetime_deposit_paid = Column(Boolean, default=False)
    monthly_due_date = Column(Date, nullable=True)

    payments = relationship("Payment", back_populates="member")
