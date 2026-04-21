import pytest
import numpy as np
from unittest.mock import patch
from ml.models.allocation_model import AllocationModel
from ml.algorithms.optimization import optimize_allocation

class TestAllocationModel:
    @pytest.fixture
    def test_model(self):
        return AllocationModel()

    @pytest.fixture
    def test_employees(self):
        return [
            {
                "id": 1,
                "name": "John Doe",
                "skills": ["Python", "FastAPI"],
                "availability": 0.8
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "skills": ["React", "JavaScript"],
                "availability": 1.0
            }
        ]

    @pytest.fixture
    def test_projects(self):
        return [
            {
                "id": 1,
                "name": "Backend API",
                "required_skills": ["Python", "FastAPI"],
                "priority": 1
            },
            {
                "id": 2,
                "name": "Frontend UI",
                "required_skills": ["React", "JavaScript"],
                "priority": 2
            }
        ]

    def test_model_initialization(self, test_model):
        assert test_model.allocation_matrix is None
        assert test_model.feature_importance == {}

    def test_skill_matching(self, test_model, test_employees, test_projects):
        matching_matrix = test_model._calculate_skill_matching(test_employees, test_projects)

        assert matching_matrix.shape == (2, 2)
        # John Doe has all skills for Backend API
        assert matching_matrix[0, 0] > 0
        # Jane Smith has all skills for Frontend UI
        assert matching_matrix[1, 1] > 0

    def test_allocation_optimization(self, test_model, test_employees, test_projects):
        with patch("ml.models.allocation_model.optimize_allocation") as mock_optimize:
            mock_optimize.return_value = np.array([[0.8, 0], [0, 1.0]])

            result = test_model.generate_allocation(test_employees, test_projects)

            assert result.shape == (2, 2)
            # John Doe allocated to Backend API at 0.8 availability
            assert result[0, 0] == 0.8
            # Jane Smith allocated to Frontend UI at full availability
            assert result[1, 1] == 1.0

    def test_explain_allocation(self, test_model, test_employees, test_projects):
        test_model.allocation_matrix = np.array([[0.8, 0], [0, 1.0]])

        with patch.object(test_model, "_calculate_skill_matching") as mock_skill_matching:
            mock_skill_matching.return_value = np.array([[1.0, 0.2], [0.3, 1.0]])

            explanation = test_model.explain_allocation(test_employees, test_projects)

            assert len(explanation) == 2
            assert explanation[0]["employee_id"] == 1
            assert explanation[0]["project_id"] == 1
            assert "skill_match" in explanation[0]
            assert explanation[1]["employee_id"] == 2
            assert explanation[1]["project_id"] == 2
