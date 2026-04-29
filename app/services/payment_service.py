from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database_config import get_db
from app.repository.members import MemberRepository
from app.repository.payments import PaymentRepository
from app.schemas.payments import PaymentCreate
from app.services.plan_resolver import PlanResolver


class PaymentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.member_repo = MemberRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.plan_resolver = PlanResolver(db)

    def record_payment(self, schema: PaymentCreate):
        member = self.member_repo.read_one(schema.member_id)

        payment = self.payment_repo.create(schema)

        updated_member = self.plan_resolver.resolve(member, payment)

        return {"member": updated_member, "payment": payment}
