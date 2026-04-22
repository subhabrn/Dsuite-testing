# Allocations API

## Overview

This document provides details on the Allocations API endpoints.

## Base URL

```
/api/v1/allocations
```

## Endpoints

### GET /api/v1/allocations

Retrieves a list of allocations.

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

### GET /api/v1/allocations/{id}

Retrieves a specific allocations item by ID.

#### Response

```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/allocations

Creates a new allocations item.

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
