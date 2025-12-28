# Phase 1 – Frontend Design Documentation

Project: **IE-ticket-reservation**
Phase: **Frontend (UI/UX & Page Flow Design)**

---

## 1. Overview

This document describes the complete **Frontend design (Phase 1)** of the IE-ticket-reservation system.
The purpose of this phase is to define **user flows, page structure, and low‑fidelity wireframes** that are fully aligned with the backend conceptual design and business rules.

This document is intended to be stored in the project repository as a reference for:

* Frontend implementation
* API integration testing
* Academic evaluation

---

## 2. Actors

### 2.1 Passenger (User)

A registered user of the system who can:

* View and search trips
* View trip details
* Select seats
* Create reservations (no payment)
* View booking history
* Cancel active reservations before departure

### 2.2 Administrator (Admin)

A privileged user who can:

* Create, edit, and cancel trips
* View and cancel any reservation (administrative override)
* Manage user accounts (activate/deactivate)

---

## 3. Frontend Pages (Scope)

### Authentication

* `/login`
* `/register`

### Passenger Pages

* `/trips` – Trip List
* `/trips/:tripId` – Trip Details
* `/trips/:tripId/seats` – Seat Selection
* `/bookings` – Booking History

### Admin Pages

* `/admin`
* `/admin/trips`
* `/admin/reservations`
* `/admin/users`

---

## 4. User Flow

### 4.1 Passenger Flow

1. **Login / Register**

   * Success → Trip List
   * Failure → Same page with error

2. **Trip List**

   * Search / Filter trips
   * Select a trip → Trip Details

3. **Trip Details**

   * View trip information
   * Continue to Seat Selection

4. **Seat Selection**

   * Select one or more seats
   * Confirm reservation (atomic operation)
   * Success → Booking History
   * Failure → Conflict error (seat unavailable)

5. **Booking History**

   * View reservations (active / cancelled / expired)
   * Cancel reservation (only if active and before departure)

---

### 4.2 Admin Flow

1. **Admin Login**
2. **Admin Panel**

   * Trips management
   * Reservations management (override cancel)
   * Users management

---

## 5. Wireframes (Low‑Fidelity)

### 5.1 Trip List

**Purpose:** Browse and search available trips.

**Main Components:**

* Top Navigation Bar
* Search / Filter Bar (origin, destination, date)
* Trip Cards

**Trip Card Content:**

* Origin → Destination
* Departure time
* Price
* Available seats
* Status (scheduled / cancelled)
* View button

**UI States:**

* Loading
* Empty result
* Error

---

### 5.2 Trip Details

**Purpose:** Display detailed information about a selected trip.

**Main Components:**

* Back to Trip List
* Trip header (route & departure)
* Trip information section
* Continue to Seat Selection button

**Rules:**

* Seat selection disabled if trip is cancelled or full

---

### 5.3 Seat Selection

**Purpose:** Select seats and create a reservation.

**Main Components:**

* Trip summary
* Seat legend (available / reserved / selected)
* Seat map (grid layout)
* Selected seats panel
* Confirm / Clear buttons

**Critical Rules:**

* Seat exclusivity enforced
* Atomic multi‑seat reservation
* Conflict error if any selected seat is unavailable

---

### 5.4 Booking History

**Purpose:** View and manage user reservations.

**Main Components:**

* Reservation list
* Status badge (active / cancelled / expired)
* Cancel button (only for active reservations)

**UI States:**

* Loading
* Empty history
* Error

---

### 5.5 Admin Panel

**Purpose:** Full system administration.

**Layout:**

* Top bar
* Sidebar navigation
* Main content area

**Sections:**

* Dashboard (summary)
* Trips management
* Reservations management
* Users management

**Rules:**

* Only ADMIN role allowed
* Administrative override supported

---

## 6. Business Rules Reflected in UI

* Authentication required (no guest access)
* Seat exclusivity (one active reservation per seat)
* Atomic reservation for multiple seats
* Reservation lifecycle: active / cancelled / expired
* Trip cancellation blocks new reservations
* Admin override allowed

---

## 7. Phase 1 Completion Status

✔ User flows defined
✔ All required pages designed
✔ Low‑fidelity wireframes completed
✔ Fully aligned with backend conceptual design

**Phase 1 is complete and ready for implementation.**

---

Next Phase:

* Frontend implementation (HTML/CSS/JS or framework‑based)
* API integration testing
