# Employees API

## Overview

This document provides details on the Employees API endpoints.

## Base URL

```
/api/v1/employees
```

## Endpoints

### GET /api/v1/employees

Retrieves a list of employees.

#### Request Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| page      | int  | Page number |
| limit     | int  | Items per page |

#### Response

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "limit": 10
}
```

### GET /api/v1/employees/{id}

Retrieves a specific employees item by ID.

#### Response

```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/employees

Creates a new employees item.

#### Request Body

```json
{
  "name": "string",
  "description": "string"
}
```

#### Response

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "created_at": "datetime"
}
```
