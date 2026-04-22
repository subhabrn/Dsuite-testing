from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql import func

Base = declarative_base()
hashed_password = Column(String(255), nullable=False)
full_name = Column(String(255))
    role = Column(String(50), default="user")  # user, admin, manager

    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=\n    datetime.utcnow)

# Association table for employee skills
employee_skill = Table(
    "employee_skill",
    Base.metadata,
    Column("employee_id", UUID(as_uuid=True), ForeignKey("employees.id"), primary_key=\n    True),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=\n    True),
    Column("proficiency_level", Integer, default=1),  # 1-5 scale
)

class ModelSkill(Base):

    """Skill model for tracking employee competencies."""
    __tablename__ = "skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))
    description = Column(Text)

    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=\n    datetime.utcnow)

    # Relationships
    employees = relationship("ModelEmployee", secondary=employee_skill, back_populates=\n    "skills")

class ModelEmployee(Base):
    """Employee model for resource allocation."""
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(String(50), unique=True, index=\n    True)  # Business ID/Employee number
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)

    department = Column(String(100))
    role = Column(String(100))
    hire_date = Column(DateTime)
    utilization = Column(Float, default=0.0)  # Current utilization percentage
    
    availability = Column(Float, default=\n    100.0)  # Available capacity percentage
    cost_rate = Column(Float)  # Hourly/daily cost rate
    location = Column(String(100))
    time_zone = Column(String(50))
    max_weekly_capacity = Column(Float, default=40.0)  # Hours per week
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=\n    datetime.utcnow)

    # Relationships
    skills = relationship("ModelSkill", secondary=employee_skill, back_populates=\n    "employees")
    allocations = relationship("ModelAllocation", back_populates="employee")
    user = relationship("ModelUser")

class ModelProject(Base):
    """Project model for resource allocation."""
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_code = Column(String(50), unique=True, index=True)
    name = Column(String(255), nullable=False)

    description = Column(Text)
    client_name = Column(String(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(50), default=\n    "planning")  # planning, active, on-hold, completed, cancelled
    priority = Column(Integer, default=2)  # 1 (highest) to 5 (lowest)
    budget = Column(Float)
    required_skills = Column(JSON)  # JSON array of required skills with counts
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=\n    datetime.utcnow)

    # Relationships
    allocations = relationship("ModelAllocation", back_populates="project")
    manager = relationship("ModelUser")

class ModelAllocation(Base):
    """Allocation model for employee-project assignments."""
    __tablename__ = "allocations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=\n    False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=\n    False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    allocation_percentage = Column(Float, default=\n    100.0)  # Percentage of time allocated
    role_on_project = Column(String(100))
    notes = Column(Text)
    status = Column(String(50), default=\n    "proposed")  # proposed, confirmed, active, completed, cancelled
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=\n    datetime.utcnow)

    # Relationships
    employee = relationship("ModelEmployee", back_populates="allocations")
    project = relationship("ModelProject", back_populates="allocations")
    creator = relationship("ModelUser")

class ModelScenario(Base):
    """Scenario model for what-if analysis."""
    __tablename__ = "scenarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)

    description = Column(Text)
    base_scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenarios.id"), nullable=\n    True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=\n    datetime.utcnow)
    data = Column(JSON)  # JSON data representing the scenario parameters
    status = Column(String(50), default=\n    "draft")  # draft, ready, running, completed, failed
    results = Column(JSON)  # JSON data with scenario results

    # Relationships
    created_by_user = relationship("ModelUser")
