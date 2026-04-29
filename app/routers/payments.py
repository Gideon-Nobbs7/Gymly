from fastapi import APIRouter, Depends, status

from app.repository.payments import PaymentRepository
from app.schemas.payments import Payment, PaymentCreate
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("", status_code=status.HTTP_201_CREATED)
def record_payment(schema: PaymentCreate, service: PaymentService = Depends()):
    return service.record_payment(schema)


@router.get(
    "/{member_id}", response_model=list[Payment], status_code=status.HTTP_200_OK
)
def get_member_payments(member_id: str, repo: PaymentRepository = Depends()):
    return repo.member_payments(member_id)
