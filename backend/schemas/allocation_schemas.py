from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field

class AllocationBase(BaseModel):
    employee_id: int
    project_id: int
    start_date: datetime
    end_date: datetime
    allocation_percentage: float = Field(..., gt=0, le=100)
    role: Optional[str] = None
    status: str = "active"  # active, planned, completed

    class Config:
        schema_extra = {
            "example": {
                "employee_id": 1,
                "project_id": 2,
                "start_date": "2023-01-01T00:00:00",
                "end_date": "2023-03-31T00:00:00",
                "allocation_percentage": 50,
                "role": "Developer",
                "status": "active"
            }
        }

class AllocationCreate(AllocationBase):
    pass

class AllocationUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    allocation_percentage: Optional[float] = Field(None, gt=0, le=100)
    role: Optional[str] = None
    status: Optional[str] = None

class Allocation(AllocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AllocationResponse(BaseModel):
    id: int
    employee_id: int
    project_id: int
    start_date: datetime
    end_date: datetime
    allocation_percentage: float
    role: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AllocationList(BaseModel):
    items: List[AllocationResponse]
    total: int
