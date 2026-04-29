from datetime import timedelta

from sqlalchemy.orm import Session

from app.config.settings import settings
from app.core.core import PLAN_DURATION
from app.models.payments import Payment
from app.repository.payments import PaymentRepository
from app.schemas.members import Member, MembershipStatus, PlanType, date

EXPIRY_WARNING_DAYS = settings.EXPIRY_WARNING_DAYS


def compute_expiry_date(payment: Payment):
    days = PLAN_DURATION.get(payment.payment_type)
    if days is None:
        return None
    return payment.payment_date + timedelta(days=days)


def compute_status(member: Member, db: Session) -> MembershipStatus:
    today = date.today()

    if member.plan_type == PlanType.lifetime:
        if member.monthly_due_date is None:
            return MembershipStatus.paused

        days_due_until = (member.monthly_due_date - today).days
        if days_due_until < 0:
            # pause the subscription but not expired (lifetime)
            return MembershipStatus.paused
        if days_due_until <= EXPIRY_WARNING_DAYS:
            return MembershipStatus.expiring
        return MembershipStatus.active

    last_payment = PaymentRepository(db=db).get_member_latest_payment(member.id)
    if not last_payment:
        return MembershipStatus.expired

    expiry_date = compute_expiry_date(last_payment)
    if not expiry_date:
        return MembershipStatus.expired

    days_left = (expiry_date - today).days
    if days_left < 0:
        return MembershipStatus.expired
    if days_left <= EXPIRY_WARNING_DAYS:
        return MembershipStatus.expiring
    return MembershipStatus.active


def expiry_sweep(db: Session):
    members = PaymentRepository(db=db).read_all()

    updated = 0
    for member in members:
        new_status = compute_status(member, db)
        if new_status != member.status:
            member.status = new_status
            updated += 1

    db.commit()
    return updated
