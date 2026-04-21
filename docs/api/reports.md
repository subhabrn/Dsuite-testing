# Reports API

## Overview

This document provides details on the Reports API endpoints.

## Base URL

```
/api/v1/reports
```

## Endpoints

### GET /api/v1/reports

Retrieves a list of reports.

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

### GET /api/v1/reports/{id}

Retrieves a specific reports item by ID.

#### Response

```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime"
}
```

### POST /api/v1/reports

Creates a new reports item.

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
