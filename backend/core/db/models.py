"""
Database models for the Resource Allocation AI System.
This module defines the ORM models for all database tables used in the application.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association tables for many-to-many relationships
resource_tag_association = Table(
    'resource_tag_association',
    Base.metadata,
    Column('resource_id', Integer, ForeignKey('resources.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

project_tag_association = Table(
    'project_tag_association',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    """User model representing system users with authentication and role information."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(200))
    full_name = Column(String(100))
    role = Column(String(20))  # admin, manager, resource, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    resources = relationship("Resource", back_populates="user")
    projects = relationship("Project", back_populates="owner")
    allocations = relationship("Allocation", back_populates="created_by")

class Resource(Base):
    """Resource model representing personnel that can be allocated to projects."""
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    role = Column(String(100))
    skills = Column(JSON)
    capacity = Column(Float)  # Weekly hours available
    cost_rate = Column(Float)  # Hourly cost rate
    efficiency_factor = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="resources")
    allocations = relationship("Allocation", back_populates="resource")
    tags = relationship("Tag", secondary=resource_tag_association, back_populates="resources")

class Project(Base):
    """Project model representing initiatives that require resource allocation."""
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    priority = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(20))  # planning, active, completed, on-hold
    required_skills = Column(JSON)
    budget = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="projects")
    allocations = relationship("Allocation", back_populates="project")
    tags = relationship("Tag", secondary=project_tag_association, back_populates="projects")

class Allocation(Base):
    """Allocation model representing the assignment of resources to projects."""
    __tablename__ = 'allocations'

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    hours_per_week = Column(Float)
    allocation_percentage = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    resource = relationship("Resource", back_populates="allocations")
    project = relationship("Project", back_populates="allocations")
    created_by = relationship("User", back_populates="allocations")

class Tag(Base):
    """Tag model for categorizing resources and projects."""
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    category = Column(String(50))

    # Relationships
    resources = relationship("Resource", secondary=resource_tag_association, back_populates="tags")
    projects = relationship("Project", secondary=project_tag_association, back_populates="tags")

class AllocationHistory(Base):
    """AllocationHistory model for tracking changes to allocations."""
    __tablename__ = 'allocation_history'

    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(Integer, ForeignKey("allocations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    change_type = Column(String(20))  # created, updated, deleted
    previous_data = Column(JSON)
    new_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
