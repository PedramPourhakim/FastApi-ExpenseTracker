from fastapi import status


def test_expense_detail_response_404(auth_client):
    response = auth_client.get(f"/api/v1/expenses/some_dummy_expense_id")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] is True
    assert data["status_code"] == status.HTTP_404_NOT_FOUND
    assert "not" in data["message"].lower()


def test_expense_detail_response_200(random_expense, auth_client):
    expense_obj = random_expense
    response = auth_client.get(f"/api/v1/expenses/{expense_obj.id}")
    assert response.status_code == 200


def test_expenses_delete_response_200(auth_client, random_expense):
    expense_obj = random_expense
    response1 = auth_client.delete(f"/api/v1/expenses/{expense_obj.id}")
    assert response1.status_code == 200
    response2 = auth_client.delete(f"/api/v1/expenses/{expense_obj.id}")
    assert response2.status_code == 404
    data = response2.json()
    assert data["error"] is True
    assert data["status_code"] == status.HTTP_404_NOT_FOUND
    assert "not" in data["message"].lower()
