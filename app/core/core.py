import enum
from decimal import Decimal


class PlanType(str, enum.Enum):
    monthly = "monthly"
    quarterly = "quarterly"
    lifetime = "lifetime"


class MembershipStatus(str, enum.Enum):
    active = "active"
    expiring = "expiring"
    expired = "expired"
    paused = "paused"


class PaymentType(str, enum.Enum):
    monthly = "monthly"
    quarterly = "quarterly"
    lifetime_deposit = "lifetime_deposit"
    lifetime_monthly = "lifetime_monthly"


PAYMENT_AMOUNT = {
    PaymentType.monthly: Decimal("250.00"),
    PaymentType.quarterly: Decimal("450.00"),
    PaymentType.lifetime_deposit: Decimal("600.00"),
    PaymentType.lifetime_monthly: Decimal("100.00"),
}


PLAN_DURATION = {
    PaymentType.monthly: 30,
    PaymentType.quarterly: 90,
}
