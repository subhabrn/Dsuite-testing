"""
Seed file to populate the database with initial data.
Run this after migrations.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.core.db.database import SessionLocal
from backend.core.db.models import Employee, Project, Allocation

def seed_data():
    db = SessionLocal()
    try:
        # Check if we have any employees already
        existing_employees = db.query(Employee).count()
        if existing_employees > 0:
            print("Database already contains data. Skipping seeding.")
            return

        # Create employees
        employees = [
            Employee(
                name="John Doe",
                email="john.doe@example.com",
                title="Senior Developer",
                department="Engineering",
                skills="Python, FastAPI, React",
                hourly_cost=75.0,
                availability=40.0
            ),
            Employee(
                name="Jane Smith",
                email="jane.smith@example.com",
                title="Project Manager",
                department="Project Management",
                skills="Agile, Scrum, Jira",
                hourly_cost=85.0,
                availability=40.0
            ),
            Employee(
                name="Bob Johnson",
                email="bob.johnson@example.com",
                title="Data Scientist",
                department="Data Science",
                skills="Python, Machine Learning, Statistics",
                hourly_cost=80.0,
                availability=40.0
            )
        ]
        db.add_all(employees)
        db.commit()

        # Create projects
        projects = [
            Project(
                name="Website Redesign",
                description="Redesign the company website with modern UI/UX",
                client="Acme Inc.",
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=90),
                priority=1,
                status="active",
                required_skills="React, Design, UI/UX",
                budget=50000.0
            ),
            Project(
                name="ML Pipeline",
                description="Build machine learning pipeline for data processing",
                client="Data Corp",
                start_date=datetime.utcnow() + timedelta(days=30),
                end_date=datetime.utcnow() + timedelta(days=120),
                priority=2,
                status="planned",
                required_skills="Python, Machine Learning, Data Engineering",
                budget=75000.0
            )
        ]
        db.add_all(projects)
        db.commit()

        # Create allocations
        allocations = [
            Allocation(
                employee_id=1,
                project_id=1,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=90),
                hours_per_week=30.0,
                role="Lead Developer"
            ),
            Allocation(
                employee_id=2,
                project_id=1,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=90),
                hours_per_week=20.0,
                role="Project Manager"
            ),
            Allocation(
                employee_id=3,
                project_id=2,
                start_date=datetime.utcnow() + timedelta(days=30),
                end_date=datetime.utcnow() + timedelta(days=120),
                hours_per_week=40.0,
                role="Data Scientist"
            )
        ]
        db.add_all(allocations)
        db.commit()

        print("Initial seed data successfully created!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
