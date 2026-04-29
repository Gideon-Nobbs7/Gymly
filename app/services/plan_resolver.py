"""
Runs after a payment is recorded and updates the member accordingly
"""

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.core import (PLAN_DURATION, MembershipStatus, PaymentType,
                           PlanType)
from app.core.exceptions import PlanResolverError
from app.models.members import Member
from app.models.payments import Payment


class PlanResolver:
    def __init__(self, db: Session):
        self.db = db

    def _resolve_standard(self, member: Member, payment: Payment):
        member.plan_type = (
            PlanType.monthly
            if payment.payment_type == PaymentType.monthly
            else PlanType.quarterly
        )
        member.status = MembershipStatus.active
        self.db.commit()
        return member

    def _resolve_lifetime_deposit(self, member: Member, payment: Payment):
        if member.lifetime_deposit_paid:
            raise PlanResolverError(
                f"Member {member.id} has already paid for lifetime deposit"
            )

        member.lifetime_deposit_paid = True
        member.lifetime_registered = True
        member.plan_type = PlanType.lifetime
        member.monthly_due_date = date.today() + timedelta(days=30)
        member.status = MembershipStatus.active
        self.db.commit()
        return member

    def _resolve_lifetime_monthly_subscription(self, member: Member, payment: Payment):
        if not member.lifetime_registered or not member.lifetime_deposit_paid:
            raise PlanResolverError(
                f"Member {member.id} is not a registered lifetime member"
            )

        member.monthly_due_date = date.today() + timedelta(days=30)
        member.status = MembershipStatus.active
        self.db.commit()
        return member

    def resolve(self, member: Member, payment: Payment):
        resolver = {
            PaymentType.monthly: self._resolve_standard,
            PaymentType.quarterly: self._resolve_standard,
            PaymentType.lifetime_deposit: self._resolve_lifetime_deposit,
            PaymentType.lifetime_monthly: self._resolve_lifetime_monthly_subscription,
        }.get(payment.payment_type)

        if not resolver:
            raise PlanResolverError(
                f"No resolver for payment type: {payment.payment_type}"
            )

        return resolver(member, payment)
