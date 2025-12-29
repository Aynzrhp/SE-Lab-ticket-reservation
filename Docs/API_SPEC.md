# API_SPEC.md

Project: IE-ticket-reservation  
Phase: Backend - Phase 2 (API Contract)  
Last Updated: 2025-12-29  

## 1. Overview

This document defines the REST API contract between frontend and backend for the IE-ticket-reservation system.

It is aligned with:

- Backend conceptual entities & business rules (User, Trip, Seat, Reservation; no payment; atomic multi-seat reservation; seat exclusivity).
- Frontend page flow (Login/Register, Trip List, Trip Details, Seat Selection, Booking History).
- Admin operations are handled via Django Admin (`/admin/`) and are outside the REST API contract.

Key actors:

- Passenger (USER): browse/search trips, view details, select seats, create reservations, view booking history, cancel active reservations before departure.
- Administrator: uses Django Admin panel (no admin REST endpoints in this spec).

## 2. Base URL & Conventions

### 2.1 Base URL

- Base: `/api`

### 2.2 Content Types

- Request/Response: `application/json; charset=utf-8`

### 2.3 Authentication

- JWT Bearer token required for all endpoints except:
  - `POST /auth/register`
  - `POST /auth/login`
- Header:
  - `Authorization: Bearer <access_token>`

### 2.4 Date/Time Format

- All timestamps are ISO 8601 strings.  
  Example: `2026-01-20T08:30:00Z`

### 2.5 Pagination (for list endpoints)

Query params:

- `page` (default: 1)
- `page_size` (default: 10, max: 50)

Response metadata:

```json
{
  "meta": { "page": 1, "page_size": 10, "total": 123 }
}
```

### 2.6 Sorting (optional)

Sorting can be supported later:

- sort=departure_time
- order=asc|desc

## 3. Common Data Models

### 3.1

```json
{
  "user_id": 10,
  "name": "Erfan Zamani",
  "phone": "+98**********",
  "role": "USER",
  "created_at": "2025-12-29T09:00:00Z"
}
```

### 3.2 Trip

```json
{
  "trip_id": 501,
  "origin": "Ardabil",
  "destination": "Tehran",
  "departure_time": "2026-01-20T08:30:00Z",
  "price": 450000,
  "status": "scheduled",
  "total_seats": 44,
  "available_seats": 12
}
```

### 3.3 Seat

```json
{
  "seat_id": 12001,
  "seat_number": "12",
  "trip_id": 501,
  "status": "available"
}
```

### 3.4 Reservation

```json
{
  "reservation_id": 9001,
  "user_id": 10,
  "trip_id": 501,
  "status": "active",
  "seat_ids": [12001, 12002],
  "created_at": "2025-12-29T10:10:00Z",
  "cancelled_at": null
}
```

Statuses:

Reservation: active | cancelled | expired
Trip: scheduled | cancelled
Seat: available | reserved

## 4. Error Format (Unified)

All error responses MUST follow this format:

```json
{
  "error": {
    "code": "SEAT_CONFLICT",
    "message": "One or more seats are already reserved.",
    "details": {
      "seat_ids": [12001, 12002]
    }
  }
}
```

### 4.1 Standard Error Codes

- VALIDATION_ERROR (400)
- AUTH_REQUIRED (401)
- AUTH_INVALID (401)
- FORBIDDEN (403)
- NOT_FOUND (404)
- CONFLICT (409)
- SEAT_CONFLICT (409)
- TRIP_CANCELLED (409)
- TRIP_FULL (409)
- RESERVATION_NOT_CANCELLABLE (409)

## 5. Authentication

### 5.1 Register

POST /auth/register
Request:

```json
{
  "name": "Erfan Zamani",
  "phone": "+98**********",
  "password": "StrongPassword123!"
}
```

Response (201):

```json
{
  "access_token": "<jwt>",
  "user": {
    "user_id": 10,
    "name": "Erfan Zamani",
    "phone": "+98**********",
    "role": "USER",
    "created_at": "2025-12-29T09:00:00Z"
  }
}
```

Errors:

- 400 VALIDATION_ERROR (invalid phone/password format)
- 409 CONFLICT (phone already exists)

### 5.2 Login

POST /auth/login
Request:

```json
{
  "phone": "+98**********",
  "password": "StrongPassword123!"
}
```

Response (200):

```json
{
  "access_token": "<jwt>",
  "user": {
    "user_id": 10,
    "name": "Erfan Zamani",
    "phone": "+98**********",
    "role": "USER",
    "created_at": "2025-12-29T09:00:00Z"
  }
}
```

Errors:

- 401 AUTH_INVALID (wrong credentials)

Errors:

401 AUTH_INVALID (wrong credentials)

## 6. Trips

### 6.1 List / Search Trips

GET /trips

#### Query params (all optional)

- origin (string)
- destination (string)
- date (YYYY-MM-DD), e.g. 2026-01-20
- page, page_size

Example:

GET /trips?origin=Ardabil&destination=Tehran&date=2026-01-20&page=1&page_size=10

Response (200):

```json
{
  "meta": { "page": 1, "page_size": 10, "total": 2 },
  "items": [
    {
      "trip_id": 501,
      "origin": "Ardabil",
      "destination": "Tehran",
      "departure_time": "2026-01-20T08:30:00Z",
      "price": 450000,
      "status": "scheduled",
      "total_seats": 44,
      "available_seats": 12
    }
  ]
}

```

Errors:

- 401 AUTH_REQUIRED / AUTH_INVALID

### 6.2 Trip Details

GET /trips/{tripId}

Response (200):

```json
{
  "trip": {
    "trip_id": 501,
    "origin": "Ardabil",
    "destination": "Tehran",
    "departure_time": "2026-01-20T08:30:00Z",
    "price": 450000,
    "status": "scheduled",
    "total_seats": 44,
    "available_seats": 12
  }
}
```

Errors:

- 401 AUTH_REQUIRED / AUTH_INVALID
- 404 NOT_FOUND

## 7. Seats (Availability)

### 7.1 Seat Map for a Trip

GET /trips/{tripId}/seats

Response (200):

```json
{
  "trip_id": 501,
  "items": [
    { "seat_id": 12001, "seat_number": "1", "status": "available" },
    { "seat_id": 12002, "seat_number": "2", "status": "reserved" }
  ]
}
```

Notes:

- This endpoint should reflect real-time availability.
- Conflicts are ultimately enforced at reservation creation time (see POST /reservations).

Errors:

- 401 AUTH_REQUIRED / AUTH_INVALID
- 404 NOT_FOUND (trip not found)

## 8. Reservations

Business rules enforced:

- Seat exclusivity: a seat cannot be reserved by more than one active reservation.
- Atomic multi-seat reservation: if any seat is unavailable, the entire request is rejected.
- Trip consistency: all seats must belong to the same trip.
- Cancel allowed only if reservation is active and before trip departure time.

### 8.1 Create Reservation (Atomic)

POST /reservations

Request:

```json
{
  "trip_id": 501,
  "seat_ids": [12001, 12003]
}
```

Response (201):

```json
{
  "reservation": {
    "reservation_id": 9001,
    "user_id": 10,
    "trip_id": 501,
    "status": "active",
    "seat_ids": [12001, 12003],
    "created_at": "2025-12-29T10:10:00Z",
    "cancelled_at": null
  }
}
```

Errors:

- 400 VALIDATION_ERROR (empty seat_ids, invalid format)
- 404 NOT_FOUND (trip not found OR seat not found)
- 409 TRIP_CANCELLED (trip status is cancelled)
- 409 TRIP_FULL (available_seats == 0)
- 409 SEAT_CONFLICT (one or more seats already reserved)

Example SEAT_CONFLICT:

```json
{
  "error": {
    "code": "SEAT_CONFLICT",
    "message": "One or more seats are already reserved.",
    "details": { "seat_ids": [12001] }
  }
}
```

- 409 CONFLICT (seats do not belong to trip_id)
- 401 AUTH_REQUIRED / AUTH_INVALID

### 8.2 List My Reservations (Booking History)

GET /reservations

#### Query params (optional)

- status = active|cancelled|expired
- page, page_size

Response (200):

```JSON
{
  "meta": { "page": 1, "page_size": 10, "total": 3 },
  "items": [
    {
      "reservation_id": 9001,
      "trip_id": 501,
      "status": "active",
      "seat_ids": [12001, 12003],
      "created_at": "2025-12-29T10:10:00Z"
    }
  ]
}
```

Errors:

401 AUTH_REQUIRED / AUTH_INVALID

### 8.3 Get Reservation Details (Optional)

GET /reservations/{reservationId}

#### Rules

USER can access only their own reservation.

Response (200):

```json
{
  "reservation": {
    "reservation_id": 9001,
    "user_id": 10,
    "trip_id": 501,
    "status": "active",
    "seat_ids": [12001, 12003],
    "created_at": "2025-12-29T10:10:00Z",
    "cancelled_at": null
  }
}
```

Errors:

- 401 AUTH_REQUIRED / AUTH_INVALID
- 403 FORBIDDEN (user tries to access others)
- 404 NOT_FOUND

### 8.4 Cancel Reservation

DELETE /reservations/{reservationId}

#### Rules

USER can cancel only if:

reservation.status == active
current_time < trip.departure_time

Response (200):

```json
{
  "reservation": {
    "reservation_id": 9001,
    "status": "cancelled",
    "cancelled_at": "2025-12-29T10:40:00Z"
  }
}
```

Errors:

- 401 AUTH_REQUIRED / AUTH_INVALID
- 403 FORBIDDEN
- 404 NOT_FOUND
- 409 RESERVATION_NOT_CANCELLABLE (already cancelled/expired, or after departure)

Example RESERVATION_NOT_CANCELLABLE:

```json
{
  "error": {
    "code": "RESERVATION_NOT_CANCELLABLE",
    "message": "Reservation cannot be cancelled at this time.",
    "details": { "reason": "AFTER_DEPARTURE" }
  }
}
```

## 9. Admin Operations

Admin operations are handled in Django default admin panel at /admin/.
No admin REST endpoints are defined in this API contract.
