# 🎟️ Project Proposal  
## Ticket Reservation System  

### 👥 Team Members
- [Aynaz Rahmani Parhizkar](https://github.com/Aynzrhp)  
- [Erfan Zamani](https://github.com/erfnzmn)  
- **Repository:** [github.com/Aynzrhp/SE-Lab-ticket-reservation](https://github.com/Aynzrhp/SE-Lab-ticket-reservation)

---

## 📝 Project Description
The **Ticket Reservation System** is a web-based application designed to simplify and automate the process of booking travel tickets for passengers.  

The system allows users to:
- Register and log in  
- Search and filter available trips  
- Select seats  
- Make secure reservations  
- View booking history  
- Manage their profiles  

Administrators can:
- Manage trips  
- Monitor user activity  
- Handle invalid reservations  
- Control user accounts  

This project aims to deliver a **secure**, **user-friendly**, and **efficient** platform that:
- Eliminates manual ticket management complexity  
- Prevents overbooking  
- Enhances the customer experience  

The backend will include **robust authentication (JWT)**, **reliable session management**, and **role-based access control** for both users and administrators.

---

## 🚀 User Stories

### 🧍 Section: Customers / Passengers

#### 1. Register Account  
**User Story:**  
> As a new user, I want to create an account with my phone number and password, so that I can access ticket booking features securely.  

**Description:**  
The system should allow new users to create an account to access ticket booking, payment, and reservation history. The process includes phone validation and secure password storage.

---

#### 2. Login  
**User Story:**  
> As a registered user, I want to log into my account, so that I can manage my reservations and profile information.  

**Description:**  
Users log in using their credentials to access booking, history, and profile settings. Authentication must use secure **JWT-based** tokens.

---

#### 3. View Trip List  
**User Story:**  
> As a user, I want to browse a list of available trips, so that I can choose a suitable destination and date.  

**Description:**  
Displays all available trips with details such as origin, destination, date, and price — dynamically fetched from the database.

---

#### 4. Search and Filter Trips  
**User Story:**  
> As a user, I want to search for trips by origin, destination, and date, so that I can find my desired trip easily.  

**Description:**  
Allows quick search and filtering of trips based on parameters like departure city, destination, and travel date.

---

#### 5. View Trip Details  
**User Story:**  
> As a user, I want to view detailed information about a trip (price, time, available seats), so that I can make an informed booking decision.  

**Description:**  
Shows full trip information: remaining seats, vehicle type, travel time, and total price.

---

#### 6. Select Seat  
**User Story:**  
> As a user, I want to select my preferred seat from a seat map, so that I can travel comfortably.  

**Description:**  
Displays a visual seat layout where users can pick their preferred seat. Reserved seats appear as unavailable.

---

#### 7. Reserve Ticket  
**User Story:**  
> As a user, I want to reserve a ticket for a chosen trip, so that I can confirm my seat and plan my journey.  

**Description:**  
Reserving a ticket locks the seat temporarily until payment is confirmed, preventing double booking.

---

#### 8. View Booking History  
**User Story:**  
> As a user, I want to see all my past and upcoming bookings, so that I can manage or review my travel plans.  

**Description:**  
Displays all past and upcoming reservations with their statuses: pending, confirmed, or cancelled.

---

#### 9. Cancel Booking  
**User Story:**  
> As a user, I want to cancel my booking before departure, so that I can get a refund or reschedule my trip.  

**Description:**  
Allows users to cancel bookings before the departure date, updates seat availability, and processes refunds.

---

#### 10. Update Profile  
**User Story:**  
> As a user, I want to update my personal information (name, phone, password), so that I can keep my profile accurate and up to date.  

**Description:**  
Users can edit their name, phone number, etc., for accurate communication and updates.

---

### 🛠️ Section: Administrator

#### 12. Manage Trips  
**User Story:**  
> As an admin, I want to add, edit, or delete trips, so that I can keep trip information up to date.  

**Description:**  
Admins can create, modify, or remove trips to maintain current and accurate travel schedules.

---

#### 13. View All Reservations  
**User Story:**  
> As an admin, I want to view all ticket reservations, so that I can monitor and manage the booking system.  

**Description:**  
Admins have full visibility over all reservations, including payment and status details.

---

#### 14. Cancel Invalid Reservations  
**User Story:**  
> As an admin, I want to cancel unpaid bookings, so that I can free up seats for other users.  

**Description:**  
Admins can cancel unpaid reservations after a set time limit, releasing seats for others.

---

#### 15. Manage User Accounts  
**User Story:**  
> As an admin, I want to manage user accounts, so that I can control access to the system.  

**Description:**  
Admins can activate, deactivate, or remove users to maintain system security and prevent misuse.

---

## 🧩 Conclusion
This proposal outlines the functional requirements for a **comprehensive ticket reservation system** that serves both passengers and administrators.  
It emphasizes **security**, **usability**, and **efficiency** — ensuring a smooth and reliable user experience.
