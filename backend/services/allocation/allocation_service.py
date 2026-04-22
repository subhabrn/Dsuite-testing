from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.core.db.models import Allocation, Employee, Project
from backend.schemas import allocation_schemas
from backend.core.errors import exceptions
from backend.services.notification import notification_service

class AllocationService:
    @staticmethod
    async def create_allocation(db: Session, allocation: allocation_schemas.AllocationCreate) -> Allocation:
        """
        Create a new resource allocation
        """
        # Verify employee exists
        employee = db.query(Employee).filter(Employee.id == allocation.employee_id).first()
        if not employee:
            raise exceptions.NotFoundException(f"Employee with id {allocation.employee_id} not found")

        # Verify project exists
        project = db.query(Project).filter(Project.id == allocation.project_id).first()
        if not project:
            raise exceptions.NotFoundException(f"Project with id {allocation.project_id} not found")

        # Check if employee is already allocated for the given time period
        await AllocationService._validate_allocation_conflicts(
            db,
            employee_id=allocation.employee_id,
            start_date=allocation.start_date,
            end_date=allocation.end_date,
            allocation_percentage=allocation.allocation_percentage
        )

        db_allocation = Allocation(
            employee_id=allocation.employee_id,
            project_id=allocation.project_id,
            start_date=allocation.start_date,
            end_date=allocation.end_date,
            allocation_percentage=allocation.allocation_percentage,
            role=allocation.role,
            status=allocation.status
        )

        db.add(db_allocation)
        db.commit()
        db.refresh(db_allocation)

        # Send notification about the new allocation
        await notification_service.send_allocation_notification(
            employee_id=allocation.employee_id,
            project_id=allocation.project_id,
            event_type="allocation_created"
        )

        return db_allocation

    @staticmethod
    async def get_allocation(db: Session, allocation_id: int) -> Allocation:
        """
        Get allocation by ID
        """
        allocation = db.query(Allocation).filter(Allocation.id == allocation_id).first()
        if not allocation:
            raise exceptions.NotFoundException(f"Allocation with id {allocation_id} not found")
        return allocation

    @staticmethod
    async def get_allocations(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        employee_id: Optional[int] = None,
        project_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all allocations with optional filtering
        """
        query = db.query(Allocation)

        if employee_id is not None:
            query = query.filter(Allocation.employee_id == employee_id)

        if project_id is not None:
            query = query.filter(Allocation.project_id == project_id)

        if status is not None:
            query = query.filter(Allocation.status == status)

        total = query.count()
        allocations = query.offset(skip).limit(limit).all()

        return {
            "items": allocations,
            "total": total
        }

    @staticmethod
    async def update_allocation(
        db: Session,
        allocation_id: int,
        allocation_data: allocation_schemas.AllocationUpdate
    ) -> Allocation:
        """
        Update an allocation
        """
        db_allocation = await AllocationService.get_allocation(db, allocation_id)

        update_data = allocation_data.dict(exclude_unset=True)

        # Check for allocation conflicts if updating dates or percentage
        if "start_date" in update_data or "end_date" in update_data or "allocation_percentage" in update_data:
            start_date = update_data.get("start_date", db_allocation.start_date)
            end_date = update_data.get("end_date", db_allocation.end_date)
            allocation_percentage = update_data.get("allocation_percentage", db_allocation.allocation_percentage)

            await AllocationService._validate_allocation_conflicts(
                db,
                employee_id=db_allocation.employee_id,
                start_date=start_date,
                end_date=end_date,
                allocation_percentage=allocation_percentage,
                exclude_allocation_id=allocation_id
            )

        # Update allocation fields
        for key, value in update_data.items():
            setattr(db_allocation, key, value)

        db_allocation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_allocation)

        # Send notification about the updated allocation
        await notification_service.send_allocation_notification(
            employee_id=db_allocation.employee_id,
            project_id=db_allocation.project_id,
            event_type="allocation_updated"
        )

        return db_allocation

    @staticmethod
    async def delete_allocation(db: Session, allocation_id: int) -> Dict[str, Any]:
        """
        Delete an allocation
        """
        db_allocation = await AllocationService.get_allocation(db, allocation_id)

        employee_id = db_allocation.employee_id
        project_id = db_allocation.project_id

        db.delete(db_allocation)
        db.commit()

        # Send notification about the deleted allocation
        await notification_service.send_allocation_notification(
            employee_id=employee_id,
            project_id=project_id,
            event_type="allocation_deleted"
        )

        return {"message": f"Allocation {allocation_id} successfully deleted"}

    @staticmethod
    async def _validate_allocation_conflicts(
        db: Session,
        employee_id: int,
        start_date: datetime,
        end_date: datetime,
        allocation_percentage: float,
        exclude_allocation_id: Optional[int] = None
    ) -> None:
        """
        Check if the allocation would create a conflict (over-allocation)
        """
        # Get all active allocations for this employee that overlap with the time period
        query = (
            db.query(Allocation)
            .filter(Allocation.employee_id == employee_id)
            .filter(Allocation.status.in_(["active", "planned"]))
            .filter(Allocation.start_date <= end_date)
            .filter(Allocation.end_date >= start_date)
        )

        if exclude_allocation_id:
            query = query.filter(Allocation.id != exclude_allocation_id)

        overlapping_allocations = query.all()

        # Check each day in the date range for over-allocation
        current_date = start_date
        while current_date <= end_date:
            total_allocation_for_day = allocation_percentage

            for allocation in overlapping_allocations:
                if allocation.start_date <= current_date <= allocation.end_date:
                    total_allocation_for_day += allocation.allocation_percentage

            if total_allocation_for_day > 100:
                raise exceptions.BadRequestException(
                    f"Employee would be over-allocated ({total_allocation_for_day}%) on {current_date.date()}"
                )

            current_date = current_date.replace(day=current_date.day + 1)
