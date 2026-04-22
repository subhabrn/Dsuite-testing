from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from backend.core.db.models import Scenario, Allocation, Employee, Project
from backend.schemas import scenario_schemas
from backend.core.errors import exceptions

class ScenarioService:
    @staticmethod
    async def create_scenario(db: Session, scenario: scenario_schemas.ScenarioCreate) -> Scenario:
        """
        Create a new allocation scenario
        """
        # Create the scenario record
        db_scenario = Scenario(
            name=scenario.name,
            description=scenario.description,
            created_by=scenario.created_by,
            is_active=scenario.is_active,
            allocation_data=scenario.allocation_data
        )

        db.add(db_scenario)
        db.commit()
        db.refresh(db_scenario)

        return db_scenario

    @staticmethod
    async def get_scenario(db: Session, scenario_id: int) -> Scenario:
        """
        Get scenario by ID
        """
        scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
        if not scenario:
            raise exceptions.NotFoundException(f"Scenario with id {scenario_id} not found")
        return scenario

    @staticmethod
    async def get_scenarios(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        created_by: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get all scenarios with optional filtering
        """
        query = db.query(Scenario)

        if created_by is not None:
            query = query.filter(Scenario.created_by == created_by)

        if is_active is not None:
            query = query.filter(Scenario.is_active == is_active)

        total = query.count()
        scenarios = query.offset(skip).limit(limit).all()

        return {
            "items": scenarios,
            "total": total
        }

    @staticmethod
    async def update_scenario(
        db: Session,
        scenario_id: int,
        scenario_data: scenario_schemas.ScenarioUpdate
    ) -> Scenario:
        """
        Update a scenario
        """
        db_scenario = await ScenarioService.get_scenario(db, scenario_id)

        update_data = scenario_data.dict(exclude_unset=True)

        # If scenario is being set to active, deactivate all other scenarios
        if update_data.get("is_active"):
            other_active_scenarios = (
                db.query(Scenario)
                .filter(Scenario.id != scenario_id, Scenario.is_active == True)
                .all()
            )
            for other_scenario in other_active_scenarios:
                other_scenario.is_active = False

        # Update scenario fields
        for key, value in update_data.items():
            setattr(db_scenario, key, value)

        db_scenario.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_scenario)

        return db_scenario

    @staticmethod
    async def delete_scenario(db: Session, scenario_id: int) -> Dict[str, Any]:
        """
        Delete a scenario
        """
        db_scenario = await ScenarioService.get_scenario(db, scenario_id)

        # Cannot delete active scenarios
        if db_scenario.is_active:
            raise exceptions.BadRequestException("Cannot delete an active scenario. Set it to inactive first.")

        db.delete(db_scenario)
        db.commit()

        return {"message": f"Scenario {scenario_id} successfully deleted"}

    @staticmethod
    async def apply_scenario(db: Session, scenario_id: int) -> Dict[str, Any]:
        """
        Apply a scenario by creating actual allocations from it
        """
        scenario = await ScenarioService.get_scenario(db, scenario_id)
        allocation_data = scenario.allocation_data

        # Validate that all referenced employees and projects exist
        for allocation in allocation_data.get("allocations", []):
            employee_id = allocation.get("employee_id")
            project_id = allocation.get("project_id")

            employee = db.query(Employee).filter(Employee.id == employee_id).first()
            if not employee:
                raise exceptions.NotFoundException(f"Employee with id {employee_id} not found")

            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise exceptions.NotFoundException(f"Project with id {project_id} not found")

        # Create allocations
        created_allocations = []
        for allocation_item in allocation_data.get("allocations", []):
            db_allocation = Allocation(
                employee_id=allocation_item.get("employee_id"),
                project_id=allocation_item.get("project_id"),
                start_date=datetime.fromisoformat(allocation_item.get("start_date")),
                end_date=datetime.fromisoformat(allocation_item.get("end_date")),
                allocation_percentage=allocation_item.get("allocation_percentage"),
                role=allocation_item.get("role"),
                status="planned"
            )

            db.add(db_allocation)
            created_allocations.append(db_allocation)

        db.commit()

        return {
            "message": f"Successfully applied scenario {scenario_id}",
            "allocations_created": len(created_allocations)
        }

    @staticmethod
    async def compare_scenarios(
        db: Session,
        scenario_id_1: int,
        scenario_id_2: int
    ) -> scenario_schemas.ScenarioComparison:
        """
        Compare two scenarios and return differences
        """
        scenario1 = await ScenarioService.get_scenario(db, scenario_id_1)
        scenario2 = await ScenarioService.get_scenario(db, scenario_id_2)

        differences = {
            "name": {
                "scenario1": scenario1.name,
                "scenario2": scenario2.name
            },
            "description": {
                "scenario1": scenario1.description,
                "scenario2": scenario2.description
            },
            "allocation_count": {
                "scenario1": len(scenario1.allocation_data.get("allocations", [])),
                "scenario2": len(scenario2.allocation_data.get("allocations", []))
            },
            "resource_utilization": {
                "scenario1": ScenarioService._calculate_utilization(scenario1.allocation_data),
                "scenario2": ScenarioService._calculate_utilization(scenario2.allocation_data)
            },
            "project_coverage": {
                "scenario1": ScenarioService._calculate_project_coverage(scenario1.allocation_data),
                "scenario2": ScenarioService._calculate_project_coverage(scenario2.allocation_data)
            }
        }

        return scenario_schemas.ScenarioComparison(
            scenario_id_1=scenario_id_1,
            scenario_id_2=scenario_id_2,
            differences=differences
        )

    @staticmethod
    def _calculate_utilization(allocation_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate resource utilization from allocation data
        """
        # This is a simplified version - in a real implementation,
        # this would calculate employee utilization over time
        employee_utilization = {}

        for allocation in allocation_data.get("allocations", []):
            employee_id = allocation.get("employee_id")
            percentage = allocation.get("allocation_percentage", 0)

            if employee_id not in employee_utilization:
                employee_utilization[employee_id] = 0

            employee_utilization[employee_id] += percentage

        return employee_utilization

    @staticmethod
    def _calculate_project_coverage(allocation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate project coverage from allocation data
        """
        # This is a simplified version - in a real implementation,
        # this would calculate project coverage metrics
        project_coverage = {}

        for allocation in allocation_data.get("allocations", []):
            project_id = allocation.get("project_id")

            if project_id not in project_coverage:
                project_coverage[project_id] = {
                    "total_allocation_percentage": 0,
                    "allocated_employees": set()
                }

            project_coverage[project_id]["total_allocation_percentage"] += allocation.get("allocation_percentage", 0)
            project_coverage[project_id]["allocated_employees"].add(allocation.get("employee_id"))

        # Convert sets to list for JSON serialization
        for project_id in project_coverage:
            project_coverage[project_id]["allocated_employees"] = list(project_coverage[project_id]["allocated_employees"])
            project_coverage[project_id]["employee_count"] = len(project_coverage[project_id]["allocated_employees"])

        return project_coverage
