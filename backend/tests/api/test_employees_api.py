import pytest
from fastapi.testclient import TestClient
from main import app
from schemas.employee import EmployeeCreate
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def test_employee():
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "department": "Engineering",
        "skills": ["Python", "FastAPI"],
        "availability": 1.0
    }

def test_get_employees(test_employee):
    with patch("services.employee.EmployeeService.get_all") as mock_get_all:
        mock_get_all.return_value = [test_employee]
        response = client.get("/api/v1/employees")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == test_employee["id"]
        assert data[0]["name"] == test_employee["name"]

def test_get_employee_by_id(test_employee):
    with patch("services.employee.EmployeeService.get_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = test_employee
        response = client.get(f"/api/v1/employees/{test_employee['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_employee["id"]
        assert data["name"] == test_employee["name"]

def test_get_employee_not_found():
    with patch("services.employee.EmployeeService.get_by_id") as mock_get_by_id:
        mock_get_by_id.return_value = None
        response = client.get("/api/v1/employees/999")

        assert response.status_code == 404

def test_create_employee(test_employee):
    with patch("services.employee.EmployeeService.create") as mock_create:
        mock_create.return_value = test_employee
        employee_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "department": "Engineering",
            "skills": ["Python", "FastAPI"],
            "availability": 1.0
        }
        response = client.post("/api/v1/employees", json=employee_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == employee_data["name"]
        assert data["email"] == employee_data["email"]
