from datetime import date, timedelta
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, model_validator

from app.core.core import MembershipStatus, PlanType


class Member(BaseModel):
    id: UUID
    name: str
    phone: str
    date_joined: date
    plan_type: PlanType
    status: MembershipStatus = MembershipStatus.active
    expiry_date: Optional[date] = None
    lifetime_registered: Optional[bool] = None
    lifetime_deposit_paid: Optional[bool] = None
    monthly_due_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_plan_type(self):
        if self.plan_type == PlanType.lifetime:
            assert self.lifetime_registered, "Lifetime plan must be registered"
            assert self.lifetime_deposit_paid, "GH₵600 deposit must be made"
            assert (
                self.monthly_due_date is not None
            ), "Lifetime member needs a monthly due date"
        return self


class MemberCreate(BaseModel):
    name: str
    phone: str
    plan_type: PlanType
    date_joined: date = date.today()


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[MembershipStatus] = None
    expiry_date: Optional[date] = None
    monthly_due_date: Optional[date] = None
