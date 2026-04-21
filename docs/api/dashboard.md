# Dashboard API

## Overview

This document provides details on the Dashboard API endpoints.

## Base URL

```
/api/v1/dashboard
```

## Endpoints

### GET /api/v1/dashboard

Retrieves a list of dashboard.

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

### GET /api/v1/dashboard/{id}

Retrieves a specific dashboard item by ID.

#### Response

```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/dashboard

Creates a new dashboard item.

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
