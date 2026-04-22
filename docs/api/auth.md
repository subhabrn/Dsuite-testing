# Auth API

## Overview

This document provides details on the Auth API endpoints.

## Base URL

```
/api/v1/auth
```

## Endpoints

### GET /api/v1/auth

Retrieves a list of auth.

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

### GET /api/v1/auth/{id}

Retrieves a specific auth item by ID.

#### Response

```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/auth

Creates a new auth item.

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
