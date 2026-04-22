from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.core.db.database import get_db
from backend.core.security import get_current_user
from backend.schemas import scenario_schemas
from backend.services.allocation import ScenarioService
from backend.services.notification import send_scenario_notification

router = APIRouter()

@router.post("/", response_model=scenario_schemas.ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario: scenario_schemas.ScenarioCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new allocation scenario
    """
    # Set created_by to current user if not specified
    if not scenario.created_by:
        scenario.created_by = current_user["id"]

    result = await ScenarioService.create_scenario(db=db, scenario=scenario)

    # Send notification about scenario creation
    await send_scenario_notification(
        scenario_id=result.id,
        user_id=current_user["id"],
        event_type="scenario_created"
    )

    return result

@router.get("/{scenario_id}", response_model=scenario_schemas.ScenarioResponse)
async def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a specific scenario by ID
    """
    return await ScenarioService.get_scenario(db=db, scenario_id=scenario_id)

@router.get("/", response_model=scenario_schemas.ScenarioList)
async def get_scenarios(
    skip: int = 0,
    limit: int = 100,
    created_by: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all scenarios with optional filtering
    """
    return await ScenarioService.get_scenarios(
        db=db,
        skip=skip,
        limit=limit,
        created_by=created_by,
        is_active=is_active
    )

@router.put("/{scenario_id}", response_model=scenario_schemas.ScenarioResponse)
async def update_scenario(
    scenario_id: int,
    scenario: scenario_schemas.ScenarioUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update an existing scenario
    """
    result = await ScenarioService.update_scenario(
        db=db,
        scenario_id=scenario_id,
        scenario_data=scenario
    )

    # Send notification about scenario update
    await send_scenario_notification(
        scenario_id=scenario_id,
        user_id=current_user["id"],
        event_type="scenario_updated"
    )

    return result

@router.delete("/{scenario_id}")
async def delete_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Delete a scenario
    """
    result = await ScenarioService.delete_scenario(db=db, scenario_id=scenario_id)

    # Send notification about scenario deletion
    await send_scenario_notification(
        scenario_id=scenario_id,
        user_id=current_user["id"],
        event_type="scenario_deleted"
    )

    return result

@router.post("/{scenario_id}/apply")
async def apply_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Apply a scenario by creating actual allocations from it
    """
    result = await ScenarioService.apply_scenario(db=db, scenario_id=scenario_id)

    # Send notification about scenario application
    await send_scenario_notification(
        scenario_id=scenario_id,
        user_id=current_user["id"],
        event_type="scenario_applied",
        additional_data={"allocations_created": result.get("allocations_created", 0)}
    )

    return result

@router.get("/compare/{scenario_id_1}/{scenario_id_2}", response_model=scenario_schemas.ScenarioComparison)
async def compare_scenarios(
    scenario_id_1: int,
    scenario_id_2: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Compare two scenarios and return differences
    """
    return await ScenarioService.compare_scenarios(
        db=db,
        scenario_id_1=scenario_id_1,
        scenario_id_2=scenario_id_2
    )
