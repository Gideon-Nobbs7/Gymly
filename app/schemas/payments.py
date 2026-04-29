from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, model_validator

from app.core.core import PAYMENT_AMOUNT, PaymentType


class Payment(BaseModel):
    id: UUID
    member_id: UUID
    payment_type: PaymentType
    amount: Decimal
    payment_date: date = date.today()
    recorded_by: Optional[str] = None

    @model_validator(mode="after")
    def validate_amount(self):
        expected = PAYMENT_AMOUNT[self.payment_type]
        assert (
            self.amount == expected
        ), f"{self.payment_type} must be GH₵{expected} but got {self.amount}"
        return self


class PaymentCreate(BaseModel):
    member_id: UUID
    payment_type: PaymentType
    payment_date: date = date.today()
    recorded_by: Optional[str] = None
