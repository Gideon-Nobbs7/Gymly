from datetime import date, timedelta
from unittest.mock import MagicMock

import pytest

from app.core.core import MembershipStatus, PlanType
from app.models.members import Member
from app.services.status_resolver import compute_status


def make_member(**kwargs):
    defaults = {
        "id": "f5979b2a-579c-4437-8898-16e053d526e0",
        "plan_type": PlanType.monthly,
        "status": MembershipStatus.active,
        "monthly_due_date": None,
        "lifetime_registered": False,
        "lifetime_deposit_paid": False,
    }
    defaults.update(kwargs)
    m = MagicMock(spec=Member)
    for key, value in defaults.items():
        setattr(m, key, value)
    return m

def test_test_lifetime_member_paused_when_overdue(db):
    member = make_member(
        plan_type=PlanType.lifetime,
        lifetime_registered=True,
        lifetime_deposit_paid=True,
        monthly_due_date=date.today() - timedelta(days=5)
    )
    assert compute_status(member, db) == MembershipStatus.paused

def test_test_lifetime_member_expiring_within_7_days(db):
    member = make_member(
        plan_type=PlanType.lifetime,
        lifetime_registered=True,
        lifetime_deposit_paid=True,
        monthly_due_date=date.today() + timedelta(days=4)
    )
    assert compute_status(member, db) == MembershipStatus.expiring