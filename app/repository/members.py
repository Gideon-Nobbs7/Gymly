import uuid

from app.core.core import MembershipStatus
from app.core.exceptions import NotFoundError
from app.models.members import Member
from app.repository.base_repository import (BaseRepository, Depends, Session,
                                            get_db)
from app.schemas.members import MemberCreate, MemberUpdate


class MemberRepository(BaseRepository):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(Member, db)

    def create_member(self, schema):
        metadata = MemberCreate(**schema.model_dump())
        return self.create(metadata)

    def update_status(self, member_id, status: MembershipStatus) -> Member:
        return self.update(member_id, MemberUpdate(status=status))

    def member_payments(self, member_id) -> Member | None:
        member = self.read_one(id=member_id)
        if not member.payments:
            raise NotFoundError(
                message="No payment reecords found",
                detail=f"Member with ID {member_id} has no payment record",
            )
        return member.payments

    def get_expiring_members(self) -> list[Member]:
        return self.read_all(
            status=MembershipStatus.expiring,
            order_by=Member.monthly_due_date.desc(),
            limit=100,
        )

    def get_expired_members(self) -> list[Member]:
        return self.read_all(
            status=MembershipStatus.expired,
            order_by=Member.monthly_due_date.desc(),
            limit=100,
        )
