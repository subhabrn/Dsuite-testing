from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.core.db.database import get_db
from backend.core.security import get_current_user
from backend.schemas import allocation_schemas
from backend.services.allocation import AllocationService

router = APIRouter()

@router.post("/", response_model=allocation_schemas.AllocationResponse, status_code=status.HTTP_201_CREATED)
async def create_allocation(
    allocation: allocation_schemas.AllocationCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new resource allocation
    """
    return await AllocationService.create_allocation(db=db, allocation=allocation)

@router.get("/{allocation_id}", response_model=allocation_schemas.AllocationResponse)
async def get_allocation(
    allocation_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a specific allocation by ID
    """
    return await AllocationService.get_allocation(db=db, allocation_id=allocation_id)

@router.get("/", response_model=allocation_schemas.AllocationList)
async def get_allocations(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = None,
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all allocations with optional filtering
    """
    return await AllocationService.get_allocations(
        db=db,
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        project_id=project_id,
        status=status
    )

@router.put("/{allocation_id}", response_model=allocation_schemas.AllocationResponse)
async def update_allocation(
    allocation_id: int,
    allocation: allocation_schemas.AllocationUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update an existing allocation
    """
    return await AllocationService.update_allocation(
        db=db,
        allocation_id=allocation_id,
        allocation_data=allocation
    )

@router.delete("/{allocation_id}")
async def delete_allocation(
    allocation_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete an allocation
    """
    return await AllocationService.delete_allocation(db=db, allocation_id=allocation_id)

@router.get("/employee/{employee_id}", response_model=allocation_schemas.AllocationList)
async def get_employee_allocations(
    employee_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all allocations for a specific employee
    """
    return await AllocationService.get_allocations(
        db=db,
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        status=status
    )

@router.get("/project/{project_id}", response_model=allocation_schemas.AllocationList)
async def get_project_allocations(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all allocations for a specific project
    """
    return await AllocationService.get_allocations(
        db=db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        status=status
    )
