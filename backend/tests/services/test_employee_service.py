import pytest
from unittest.mock import MagicMock, patch
from services.employee import EmployeeService
from schemas.employee import EmployeeCreate, EmployeeUpdate

@pytest.fixture
def employee_service():
    return EmployeeService()

@pytest.fixture
def mock_employee():
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "department": "Engineering",
        "skills": ["Python", "FastAPI"],
        "availability": 1.0
    }

def test_get_all_employees(employee_service, mock_employee):
    with patch.object(employee_service, "db") as mock_db:
        mock_db.query().all.return_value = [mock_employee]
        result = employee_service.get_all()

        assert len(result) == 1
        assert result[0] == mock_employee

def test_get_employee_by_id(employee_service, mock_employee):
    with patch.object(employee_service, "db") as mock_db:
        mock_db.query().filter().first.return_value = mock_employee
        result = employee_service.get_by_id(1)

        assert result == mock_employee

def test_get_employee_by_id_not_found(employee_service):
    with patch.object(employee_service, "db") as mock_db:
        mock_db.query().filter().first.return_value = None
        result = employee_service.get_by_id(999)

        assert result is None

def test_create_employee(employee_service, mock_employee):
    employee_data = EmployeeCreate(
        name="John Doe",
        email="john@example.com",
        department="Engineering",
        skills=["Python", "FastAPI"],
        availability=1.0
    )

    with patch.object(employee_service, "db") as mock_db:
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with patch("services.employee.Employee") as mock_employee_model:
            mock_employee_instance = MagicMock()
            mock_employee_instance.__dict__ = mock_employee
            mock_employee_model.return_value = mock_employee_instance

            result = employee_service.create(employee_data)

            assert result == mock_employee
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
