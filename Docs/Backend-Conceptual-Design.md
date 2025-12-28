1. Scope of This Phase

This phase focuses on the conceptual backend design of the Ticket Reservation System.
The goal is to identify the core data entities, define their relationships, and establish the fundamental business rules governing seat reservation behavior.

Frontend design and UI page flow are intentionally excluded from this phase.

2. Core Entities

The system consists of the following core entities:

2.1 User

Represents registered users of the system, including both passengers and administrators.

Attributes (conceptual):

user_id (Primary Key)

name

email

password_hash

role (USER / ADMIN)

status (active / inactive)

2.2 Trip

Represents a scheduled travel instance between two locations at a specific time.

Attributes (conceptual):

trip_id (Primary Key)

origin

destination

departure_time

price

status (scheduled / cancelled)

2.3 Seat

Represents a physical seat associated with a specific trip.

Attributes (conceptual):

seat_id (Primary Key)

seat_number

trip_id (Foreign Key)

status (available / reserved)

2.4 Reservation

Represents the act of booking one or more seats by a user for a specific trip.

Attributes (conceptual):

reservation_id (Primary Key)

user_id (Foreign Key)

trip_id (Foreign Key)

status (active / cancelled / expired)

created_at

Note:
The Payment entity is intentionally excluded due to the academic and non-commercial nature of the project. Seat reservation is finalized immediately after seat selection.

3. Entity Relationships

The conceptual relationships between entities are defined as follows:

A User can have multiple Reservations
(User 1 → N Reservation)

A Trip contains multiple Seats
(Trip 1 → N Seat)

Each Seat belongs to exactly one Trip
(Seat N → 1 Trip)

Each Reservation is associated with exactly one Trip

Each Reservation may include multiple Seats,
but each Seat can belong to only one active Reservation at a time

This constraint ensures consistency and prevents double booking.

4. Core Business Rules

The system enforces the following business rules:

User authentication is mandatory
All system operations require a registered and authenticated user. Guest access is not allowed.

Seat exclusivity
A seat cannot be reserved by more than one active reservation simultaneously.

Reservation status lifecycle
Each reservation has one of the following statuses:

active: The reservation is valid and seats are occupied.

cancelled: The reservation was cancelled by the user or an administrator.

expired: The trip has been completed and the reservation is no longer active.

Seat release policy
A seat becomes available for reservation only after its associated reservation is cancelled or expired.

Atomic multi-seat reservation
If a reservation request includes multiple seats and any one of them is unavailable, the entire reservation request is rejected.

Trip consistency constraint
All seats included in a reservation must belong to the same trip.

Duplicate reservation prevention
A user cannot reserve the same seat more than once.

Administrative override
Administrators have the authority to cancel or invalidate any reservation regardless of its status.

5. Conceptual ER Model Summary (Textual)

User
(User 1) —— (N Reservation)

Trip
(Trip 1) —— (N Seat)

Reservation

Linked to one User

Linked to one Trip

Includes one or more Seats

Seat

Belongs to one Trip

Can be linked to at most one active Reservation

6. Conclusion

This phase establishes a clear and consistent backend foundation for the Ticket Reservation System.
By defining core entities, enforcing strict reservation rules, and maintaining transactional consistency, the system prevents overbooking and ensures reliable seat management while remaining suitable for an academic implementation.