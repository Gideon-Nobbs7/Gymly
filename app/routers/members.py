
from fastapi import APIRouter, Depends, status

from app.core.core import MembershipStatus
from app.repository.members import MemberRepository
from app.schemas.members import Member, MemberCreate

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("", response_model=Member, status_code=status.HTTP_201_CREATED)
def create_member(schema: MemberCreate, repo: MemberRepository = Depends()):
    return repo.create_member(schema)


@router.get("/expiring", response_model=list[Member], status_code=status.HTTP_200_OK)
def get_expiring_members(repo: MemberRepository = Depends()):
    return repo.get_expiring_members()


@router.get("/expired", response_model=list[Member], status_code=status.HTTP_200_OK)
def get_expired_members(repo: MemberRepository = Depends()):
    return repo.get_expired_members()


@router.get("/{member_id}", response_model=list[Member], status_code=status.HTTP_200_OK)
def get_member(member_id: str, repo: MemberRepository = Depends()):
    # member_uuid = uuid.UUID(member_id)
    return repo.read_one(member_id)


@router.get(
    "/{member_id}/payments", response_model=list[Member], status_code=status.HTTP_200_OK
)
def get_member_payments(member_id: str, repo: MemberRepository = Depends()):
    return repo.member_payments(member_id)


@router.get("", response_model=list[Member], status_code=status.HTTP_200_OK)
def get_all_members(repo: MemberRepository = Depends()):
    return repo.read_all()


@router.patch("/{member_id}/status", status_code=status.HTTP_202_ACCEPTED)
def update_member_status(
    member_id: str, status: MembershipStatus, repo: MemberRepository = Depends()
):
    return repo.update_status(member_id, status)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: str, repo: MemberRepository = Depends()):
    return repo.delete(member_id)
