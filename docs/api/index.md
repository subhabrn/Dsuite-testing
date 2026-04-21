# API Documentation

This document provides information about the Resource Allocation AI API endpoints, request/response formats, and authentication.

## Authentication

API access requires authentication using JWT tokens. Obtain a token by sending credentials to the `/auth/login` endpoint.

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh authentication token

### Employees

- `GET /api/v1/employees` - List all employees
- `POST /api/v1/employees` - Create new employee
- `GET /api/v1/employees/{id}` - Get employee details
- `PUT /api/v1/employees/{id}` - Update employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Projects

- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Allocations

- `GET /api/v1/allocations` - List all allocations
- `POST /api/v1/allocations` - Create new allocation
- `GET /api/v1/allocations/{id}` - Get allocation details
- `PUT /api/v1/allocations/{id}` - Update allocation
- `DELETE /api/v1/allocations/{id}` - Delete allocation

### Scenarios

- `GET /api/v1/scenarios` - List all scenarios
- `POST /api/v1/scenarios` - Create new scenario
- `GET /api/v1/scenarios/{id}` - Get scenario details
- `PUT /api/v1/scenarios/{id}` - Update scenario
- `DELETE /api/v1/scenarios/{id}` - Delete scenario
- `POST /api/v1/scenarios/{id}/run` - Run scenario

### Reports

- `GET /api/v1/reports/utilization` - Get utilization reports
- `GET /api/v1/reports/allocation` - Get allocation reports
- `GET /api/v1/reports/forecast` - Get forecast reports

## Request/Response Formats

All API endpoints accept and return JSON data.

For detailed schemas and examples, refer to the endpoint-specific documentation files in this directory.
