# 🚌 TransitFlow — Bus Reservation System

A full-stack web application for booking bus tickets online. Built with **Python Flask** for the backend, **MySQL** for the database, and **HTML/CSS/JavaScript** with **Tailwind CSS** for the frontend.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Pages](#pages)
- [How It Works](#how-it-works)

---

## Overview

TransitFlow is a bus reservation system that allows users to search for available buses between stops, select specific seats, and book tickets. The system supports seat restrictions for Women and Persons with Disabilities (PWD), generates unique PNR numbers for each booking, and provides users with a complete booking history.

---

## Features

- **User Authentication** — Register and login with JWT token-based authentication
- **Bus Search** — Search for available buses between stops with dynamic dropdowns
- **Seat Selection** — Interactive seat map showing available, booked, Women-only and PWD seats
- **Seat Restrictions** — Enforces Women-only and PWD seat restrictions based on user profile
- **PNR Generation** — Unique 6-digit PNR number generated for every booking
- **Booking History** — View all past and upcoming bookings on the profile page
- **Cancel Booking** — Cancel upcoming bookings and automatically free the seat
- **Future Schedules Only** — Search results only show buses departing after the current time

---

## Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| Flask | Web framework |
| Flask-SQLAlchemy | ORM for database interaction |
| Flask-JWT-Extended | JWT authentication |
| Flask-CORS | Cross-origin resource sharing |
| PyMySQL | MySQL database driver |

### Frontend
| Technology | Purpose |
|---|---|
| HTML5 | Page structure |
| Tailwind CSS | Styling and layout |
| Font Awesome 6 | Icons |
| JavaScript (Vanilla) | API calls and page logic |

### Database
| Technology | Purpose |
|---|---|
| MySQL 8.0 | Relational database |

---

## Project Structure

```
bus_booking/
│
├── app.py                      # Main Flask application, page routes
├── config.py                   # Configuration settings and environment variables
├── models.py                   # SQLAlchemy models for all 8 database tables
│
├── routesauth.py               # API routes: /api/auth/register, /api/auth/login
├── routesbuses.py              # API routes: /api/buses/search, /api/buses/<id>/seats
├── routesbookings.py           # API routes: /api/bookings/ create, cancel, PNR lookup
│
├── static/
│   ├── js/
│   │   └── api.js              # JavaScript client — connects HTML pages to Flask API
│   └── assets/
│       ├── bus.jpeg            # Hero image for register page
│       └── bus-bg.jpeg         # Hero image for login page
│
├── templates/
│   ├── index.html              # Registration page
│   ├── login.html              # Login page
│   ├── search.html             # Bus search page with dynamic dropdowns
│   ├── select_seats.html       # Interactive seat map and booking page
│   ├── profile.html            # User profile and upcoming journey
│   └── bookings.html        # Booking confirmation and history page
│
├── database/
│   └── bus_reservation.sql     # MySQL database dump with all tables and sample data
│
├── .env                        # Environment variables (not included in repo)
├── .gitignore                  # Files excluded from Git
└── README.md                   # This file
```

---

## Database Schema

The application uses **8 tables**:

```
users           — stores user accounts (name, gender, pwd_status, email, password, phone)
buses           — stores bus details (bus_number, bus_type, total_seats)
seats           — stores individual seats (seat_type, seat_no, restriction, seat_status)
stops           — stores bus stop locations (stop_name)
routes          — stores route names (e.g. Palakkad - Kochi)
route_stops     — junction table linking routes to stops with order and distance
schedules       — stores bus schedules (bus_id, route_id, departure_time, fare)
bookings        — stores bookings (user_id, schedule_id, seat_id, pnr, total_fee)
```

### Relationships
```
buses       ──< seats        (one bus has many seats)
buses       ──< schedules    (one bus has many schedules)
routes      ──< schedules    (one route has many schedules)
routes      ──< route_stops  (one route has many stops)
stops       ──< route_stops  (one stop belongs to many routes)
users       ──< bookings     (one user has many bookings)
schedules   ──< bookings     (one schedule has many bookings)
seats       ──< bookings     (one seat has one booking at a time)
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0
- pip (Python package manager)
- Git

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/bus-booking.git
cd bus-booking
```

### Step 2 — Install Python Dependencies
```bash
pip install flask flask-sqlalchemy flask-jwt-extended flask-cors pymysql python-dotenv
```

### Step 3 — Set Up the Database
Open a terminal and import the SQL file into MySQL:
```bash
mysql -u root -pyourpassword -e "CREATE DATABASE IF NOT EXISTS BusReservationSystem;"
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -u root -pyourpassword BusReservationSystem < database\bus_reservation.sql
```

Verify the tables were created:
```bash
mysql -u root -pyourpassword -e "USE BusReservationSystem; SHOW TABLES;"
```

You should see all 8 tables:
```
bookings
buses
route_stops
routes
schedules
seats
stops
users
```

### Step 4 — Create the `.env` File
Create a file called `.env` in the project root:
```
SECRET_KEY=transitflow-secret-key-2026-secure
JWT_SECRET_KEY=transitflow-jwt-secret-key-2026-secure
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/BusReservationSystem
```
Replace `yourpassword` with your actual MySQL root password.

### Step 5 — Add Future Schedules
The sample data includes schedules from April 2026 which are now in the past. Add future schedules to see search results:
```sql
USE BusReservationSystem;

INSERT INTO schedules (bus_id, route_id, departure_time, fare) VALUES
(1, 1, '2026-06-01 08:00:00', 450.00),
(2, 2, '2026-06-01 10:30:00', 700.00),
(3, 3, '2026-06-01 21:00:00', 1200.00);
```

---

## Running the Application

```bash
python app.py
```

Open your browser and visit:
```
http://127.0.0.1:5000
```

### Sample Login Credentials
These users are included in the sample database:

| Name | Email | Password | Gender | PWD |
|---|---|---|---|---|
| Arjun Menon | arjun@gmail.com | 1234 | Male | No |
| Ananya Nair | ananya@gmail.com | 1234 | Female | No |
| Rahul Das | rahul@gmail.com | 1234 | Male | No |
| Meera Krishna | meera@gmail.com | 1234 | Female | Yes |

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/auth/register` | Register a new user | No |
| POST | `/api/auth/login` | Login and receive JWT token | No |

### Buses
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/api/buses/routes` | Get all routes with stops | No |
| GET | `/api/buses/search` | Search schedules by origin, destination, date | No |
| GET | `/api/buses/schedule/<id>` | Get a single schedule's details | No |
| GET | `/api/buses/<bus_id>/seats` | Get all seats for a bus | No |

### Bookings
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/bookings/` | Create a new booking | Yes |
| GET | `/api/bookings/my` | Get all bookings for logged-in user | Yes |
| DELETE | `/api/bookings/<id>/cancel` | Cancel a booking | Yes |
| GET | `/api/bookings/pnr/<pnr>` | Look up a booking by PNR | No |

---

## Pages

| URL | Template | Description |
|---|---|---|
| `/` | `index.html` | Homepage with navigation links |
| `/login` | `login.html` | User login page |
| `/register` | `register.html` | New user registration |
| `/search` | `search.html` | Search for buses between stops |
| `/select-seats` | `select_seats.html` | Interactive seat map for a schedule |
| `/profile` | `profile.html` | User profile and upcoming journey |
| `/my-bookings` | `my_bookings.html` | Booking confirmation and full history |

---

## How It Works

### Booking Flow
```
1. User registers or logs in
         ↓
2. Search page loads all stops from the database
         ↓
3. User selects source stop
         ↓
4. Destination dropdown updates with valid onward stops on the same route
         ↓
5. User selects destination and date → clicks Search
         ↓
6. Backend returns available buses departing after current time
         ↓
7. User clicks Select Seats → redirected to seat map
         ↓
8. Seat map loads real-time availability from database
         ↓
9. User selects a seat → booking summary appears
         ↓
10. User confirms → PNR generated → seat marked as Booked
         ↓
11. Redirected to booking confirmation page with full ticket details
```

### Authentication Flow
```
User logs in → Flask returns JWT token
      ↓
Token stored in localStorage
      ↓
Every protected API call sends: Authorization: Bearer <token>
      ↓
Flask verifies token → returns data
      ↓
Logging out clears token from localStorage
```

### Seat Restriction Logic
```
Seat restriction = "Women"  →  only Female users can book
Seat restriction = "PWD"    →  only users with pwd_status = true can book
Seat restriction = "None"   →  any user can book
```

---

## Sample Routes and Stops

| Route | Stops in Order |
|---|---|
| Palakkad - Kochi | Palakkad → Thrissur → Ernakulam → Kochi |
| Kozhikode - Trivandrum | Kozhikode → Thrissur → Ernakulam → Trivandrum |
| Thrissur - Bangalore | Thrissur → Ernakulam → Bangalore |

---

## Notes

- The `.env` file is excluded from the repository for security. Anyone cloning this project must create their own `.env` file with their database credentials.
- Passwords in the sample database are stored as hashed values using Werkzeug's `generate_password_hash`.
- JWT tokens are stored in `localStorage` and sent as Bearer tokens in the Authorization header.
- The application runs on `http://127.0.0.1:5000` by default in development mode.
