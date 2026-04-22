from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None
    created_by: int  # User ID
    is_active: bool = False

class ScenarioCreate(ScenarioBase):
    allocation_data: Dict[str, Any]  # Flexible structure for different scenario types

class ScenarioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    allocation_data: Optional[Dict[str, Any]] = None

class Scenario(ScenarioBase):
    id: int
    allocation_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ScenarioResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_by: int
    is_active: bool
    allocation_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ScenarioList(BaseModel):
    items: List[ScenarioResponse]
    total: int

class ScenarioComparison(BaseModel):
    scenario_id_1: int
    scenario_id_2: int
    differences: Dict[str, Any]
