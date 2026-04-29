import uuid

from app.models.payments import Payment
from app.repository.base_repository import (BaseRepository, Depends, Session,
                                            get_db)
from app.schemas.payments import PaymentCreate


class PaymentRepository(BaseRepository):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__(Payment, db)

    def create_payment(self, schema):
        metadata = PaymentCreate(**schema.model_dump())
        return self.create(metadata)

    def get_member_latest_payment(self, member_id) -> Payment | None:
        member_uuid = uuid.UUID(member_id)
        return self.read_where(
            member_id=member_uuid, order_by=Payment.payment_date.desc(), limit=1
        )

    def member_payments(self, member_id) -> Payment | None:
        member_uuid = uuid.UUID(member_id)
        return self.read_all(
            member_id=member_uuid, order_by=Payment.payment_date.desc()
        )
