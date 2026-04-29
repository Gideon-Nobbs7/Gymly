from datetime import date

import pytest
from fastapi import status

from app.core.core import MembershipStatus, PlanType

member_base_api = "/api/v1/members"

# fixtures
@pytest.fixture
def member_payload():
    return {
        "name": "Kwame Asante",
        "phone": "0241234567",
        "plan_type": "monthly",
        "date_joined": str(date.today())
    }

@pytest.fixture
def created_member(client, member_payload):
    response = client.post(member_base_api, json=member_payload)
    return response.json()


# tests
def test_create_member(client, member_payload):
    response = client.post(member_base_api, json=member_payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == member_payload["name"]
    assert data["plan_type"] == PlanType.monthly
    assert data["status"] == MembershipStatus.active

def test_create_duplicate_member(client, member_payload):
    response1 = client.post(member_base_api, json=member_payload)
    print(response1.json())
    response2 = client.post(member_base_api, json=member_payload)
    assert response2.status_code == status.HTTP_409_CONFLICT

def test_nonexistent_member(client):
    response = client.get(f"{member_base_api}/f5979b2a-579c-4437-8898-16e053d526e0")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_expriring_members(client, created_member):
    member_id = created_member["id"]
    # member_id = uuid.UUID(member_id)
    client.patch(
        f"{member_base_api}/{member_id}/status?status=expiring", 
    )
    response = client.get(f"{member_base_api}/expiring")
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert any(m["id"] == member_id for m in response.json())

def test_all_members(client, created_member):
    response = client.get(member_base_api)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK

def test_member_payments(client, created_member):
    member_id = created_member["id"]
    response = client.get(
        f"{member_base_api}/{member_id}/payments"
    )
    data = response.json()
    if data.get("payments"):
        assert response.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_member(client, created_member):
    member_id = created_member["id"]
    response = client.delete(f"{member_base_api}/{member_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT