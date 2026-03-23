<div align="center">

# 📚 Library Management System

### LMS — Academic Web Application

*"Streamlining library operations through smart digitization"*

🌐 Live Deployment: "https://library-management-system-10rp.onrender.com/"

Email:    admin@gmail.com
Password: admin1234

---

### 👥 Team Members

| Name | Roll No. |
|------|----------|
| Arun Raj Neupane | 080BCT006 |
| Naresh Rasaili | 080BCT022 |
| Bipin Tharu | 080BCT012 |

</div>

---

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![psycopg2](https://img.shields.io/badge/psycopg2-Raw%20SQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Executive Summary](#2-executive-summary)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [System Architecture](#5-system-architecture)
6. [Technology Stack](#6-technology-stack)
7. [Database Design](#7-database-design)
8. [Authentication & Security](#8-authentication--security)
9. [Key Features](#9-key-features)
10. [Module Descriptions](#10-module-descriptions)
11. [Pages & Routes](#11-pages--routes)
12. [Project Structure](#12-project-structure)
13. [Installation & Setup](#13-installation--setup)
14. [Environment Variables](#14-environment-variables)
15. [Team Members & Contributions](#15-team-members--contributions)

---

## 1. Project Overview

**LMS** (Library Management System) is a full-stack web application built to digitize and automate the complete lifecycle of academic library operations. It connects library staff with a powerful platform to manage books, students, and transactions — replacing slow, error-prone paper-based processes with a fast, reliable digital system.

The platform supports the full workflow: from a librarian logging in, adding an author and book to the catalog, registering a student, issuing a book to that student, and recording its return — all tracked with dates and live availability counts.

Built as an academic capstone for the **Database Management Systems** course, LMS demonstrates practical application of relational database design, **raw SQL execution via psycopg2**, server-side web development with Django, and clean frontend engineering with vanilla HTML/CSS/JS.

---

## 2. Executive Summary

LMS is architected as a **single-server Django application** that communicates with PostgreSQL exclusively through **raw SQL queries via psycopg2** — no ORM is used anywhere in the codebase. This gives the team full control over every query, making the DBMS concepts directly visible in the code.

Key technical accomplishments of the project include:

- **Normalized relational schema** designed to Third Normal Form (3NF) — author data is separated from book data, eliminating redundancy across the catalog
- **Raw SQL with psycopg2** — every database interaction is a handwritten `SELECT`, `INSERT`, or `UPDATE` executed through a `psycopg2` cursor
- **SERIAL primary keys** across all five tables with proper `REFERENCES` constraints enforcing referential integrity
- **Availability tracking** — `available_copies` is decremented on issue and incremented on return via explicit `UPDATE` statements
- **Librarian-only authentication** — a dedicated `librarian` table with credentials, separate from the student `users` entity
- **Single-page-style UI** with JavaScript-driven navigation — no full page reloads between modules

---

## 3. Problem Statement

Academic library staff frequently face the dual burden of manual record-keeping and fragmented tracking of book inventory. Physical ledgers for recording book loans, paper registers for student records, and manual overdue calculations create an environment that is error-prone, time-consuming, and impossible to audit efficiently.

There is a clear need for a **digital-first library management platform** that:

- Allows librarians to maintain a live, searchable book catalog with real-time availability
- Separates author metadata from book records for a clean, normalized catalog structure
- Provides a structured student registry linked to borrowing history
- Handles the full issue-and-return workflow with automatic date and copy tracking
- Maintains a permanent, auditable transaction log for all borrowing activity
- Offers a fast, intuitive interface requiring no technical expertise to operate

LMS is designed to address all of these challenges through principled database design and direct SQL execution.

---

## 4. Objectives

- **1** — Design and implement a normalized relational schema (3NF) covering librarians, authors, books, students, and transactions
- **2** — Execute all database operations using **raw SQL via psycopg2** — no ORM abstraction
- **3** — Build a Django backend with clean separation of concerns across views and URL routing
- **4** — Implement a secure librarian authentication system with session management and CSRF protection
- **5** — Develop an interactive frontend using HTML5, CSS3, and JavaScript with a single-page navigation pattern
- **6** — Build a real-time dashboard showing live statistics via direct `COUNT(*)` SQL queries
- **7** — Create a transaction engine that enforces `available_copies` constraints using `UPDATE` statements

---

## 5. System Architecture

LMS is built on a **Two-Tier Architecture**, separating the presentation and application logic (Django + psycopg2) from the persistence layer (PostgreSQL).

```
┌──────────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                              │
│                                                                      │
│   ┌─────────────┐   ┌──────────────┐   ┌───────────────────────┐   │
│   │  Login Page │   │  Dashboard   │   │  Books / Students /   │   │
│   │  Librarian  │   │  Stats Cards │   │  Issue-Return Forms   │   │
│   └─────────────┘   └──────────────┘   └───────────────────────┘   │
│              HTML5 · CSS3 · JavaScript (librarySystem.js)            │
└───────────────────────────────┬──────────────────────────────────────┘
                                │  HTTP Requests / JSON Responses
                                │  (fetch API)
┌───────────────────────────────▼──────────────────────────────────────┐
│                     APPLICATION LAYER                                │
│              Django 4.x — Views execute Raw SQL via psycopg2        │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────┐  │
│  │ Auth View    │  │  Book View   │  │  Student   │  │  Trans.  │  │
│  │ Raw SQL login│  │ INSERT/SELECT│  │   View     │  │   View   │  │
│  └──────────────┘  └──────────────┘  └────────────┘  └──────────┘  │
│                                                                      │
│         Django URL Router · Views · psycopg2 cursor · Admin         │
└───────────────────────────────┬──────────────────────────────────────┘
                                │  psycopg2 — Raw SQL Queries
┌───────────────────────────────▼──────────────────────────────────────┐
│                         DATA LAYER                                   │
│                 PostgreSQL · library.sql schema                      │
│                                                                      │
│  ┌───────────┐  ┌────────┐  ┌───────┐  ┌───────┐  ┌─────────────┐ │
│  │ librarian │  │ author │  │ books │  │ users │  │ issued_book │ │
│  └───────────┘  └────────┘  └───────┘  └───────┘  └─────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

### How psycopg2 is Used

Every database interaction in the application follows this pattern — a direct connection, a raw SQL string, and a cursor execution:

```python
import psycopg2

conn = psycopg2.connect(
    dbname="library", user="postgres", password="yourpassword", host="localhost"
)
cursor = conn.cursor()

# Example — fetch all books with their author names
cursor.execute("""
    SELECT b.book_id, b.book_number, b.title, a.author_name,
           b.total_copies, b.available_copies
    FROM books b
    JOIN author a ON b.author_id = a.author_id
    ORDER BY b.book_id
""")
books = cursor.fetchall()
conn.close()
```

No ORM. No model classes. Every query is handwritten SQL.

### Data Flow

```
1. Librarian logs in      ──►  SELECT * FROM librarian WHERE email=%s AND password=%s
2. Add author             ──►  INSERT INTO author (author_name) VALUES (%s)
3. Add book               ──►  INSERT INTO books (book_number, title, total_copies,
                                  available_copies, author_id) VALUES (%s,%s,%s,%s,%s)
4. Register student       ──►  INSERT INTO users (roll_no, name, batch, faculty, email)
                                  VALUES (%s,%s,%s,%s,%s)
5. Issue book             ──►  INSERT INTO issued_book (...) VALUES (...)
                               UPDATE books SET available_copies = available_copies - 1
                                  WHERE book_id = %s
6. Return book            ──►  UPDATE issued_book SET return_date=%s, status='returned'
                                  WHERE issue_id = %s
                               UPDATE books SET available_copies = available_copies + 1
                                  WHERE book_id = %s
7. Dashboard              ──►  SELECT COUNT(*) FROM books
                               SELECT COUNT(*) FROM users
                               SELECT COUNT(*) FROM issued_book WHERE status='issued'
```

---

## 6. Technology Stack

### 6.1 Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **HTML5** | Latest | Semantic page structure and form markup |
| **CSS3** | Latest | Sidebar layout, card components, responsive design |
| **JavaScript** | ES6+ | SPA-style navigation, fetch API calls, DOM updates |

### 6.2 Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.x | Core programming language |
| **Django** | 4.x | Web framework — views, URL routing, sessions, admin |
| **psycopg2** | 2.x | PostgreSQL adapter — executes all raw SQL queries |

### 6.3 Database

| Technology | Version | Purpose |
|------------|---------|---------|
| **PostgreSQL** | 15+ | Relational database (schema: `library.sql`) |
| **Raw SQL** | — | All queries handwritten — SELECT, INSERT, UPDATE |
| **SERIAL** | PG built-in | Auto-incrementing primary keys across all tables |

### 6.4 DevOps & Tooling

| Tool | Purpose |
|------|---------|
| **Git** | Version control and collaboration |
| **Django StaticFiles** | Serving CSS, JS, and image assets |
| **pip / venv** | Python dependency and environment management |

---

## 7. Database Design

The database schema is designed to **Third Normal Form (3NF)**, eliminating transitive dependencies across all entities. Five primary tables manage the full application domain — all queried directly with handwritten SQL.

### 7.1 Entity Overview

**`librarian`** is the authentication entity. Stores staff credentials — name, email, and password. Only librarians can log in. Kept entirely separate from the `users` (student) table, making the role boundary explicit at the schema level.

**`users`** represents students registered in the library system. Each student is identified by `roll_no` and academic details (`batch`, `faculty`). This entity is the borrower in all transactions.

**`author`** is a normalized entity that separates author metadata from book records. A single author can be linked to many books — eliminating repeated author name data in the `books` table (3NF compliance).

**`books`** represents the catalog of available titles. Each book holds a `title`, `book_number`, `total_copies`, `available_copies`, and a `author_id` foreign key. The `available_copies` field is the live counter — decremented on issue, incremented on return via `UPDATE` statements.

**`issued_book`** is the central transaction entity. Each row records a single borrow event — `user_id`, `book_id`, `issue_date`, `return_date`, and `status`. A `NULL` `return_date` means the book is still on loan.

### 7.2 Full Schema

```sql
-- Librarian (staff authentication)
CREATE TABLE librarian (
    librarian_id SERIAL PRIMARY KEY,
    name         VARCHAR(50),
    email        VARCHAR(50) UNIQUE,
    password     VARCHAR(100)
);

-- Users (students / borrowers)
CREATE TABLE users (
    user_id  SERIAL PRIMARY KEY,
    roll_no  VARCHAR(20),
    name     VARCHAR(50),
    batch    VARCHAR(10),
    faculty  VARCHAR(10),
    email    VARCHAR(50) UNIQUE
);

-- Author (normalized — separate from books)
CREATE TABLE author (
    author_id   SERIAL PRIMARY KEY,
    author_name VARCHAR(100)
);

-- Books (catalog with live availability counter)
CREATE TABLE books (
    book_id          SERIAL PRIMARY KEY,
    book_number      VARCHAR(29),
    title            VARCHAR(100),
    total_copies     INT,
    available_copies INT,
    author_id        INT REFERENCES author(author_id)
);

-- Issued Book (transaction / borrow record)
CREATE TABLE issued_book (
    issue_id    SERIAL PRIMARY KEY,
    issue_date  DATE,
    return_date DATE,           -- NULL = still issued
    status      VARCHAR(10),    -- 'issued' | 'returned'
    user_id     INT REFERENCES users(user_id),
    book_id     INT REFERENCES books(book_id)
);

-- Default librarian seed
INSERT INTO librarian (name, email, password)
VALUES ('Arun Neupane', 'arun123@gmail.com', 'arun123');
```

### 7.3 Entity-Relationship Diagram

```
┌─────────────┐        ┌──────────────┐        ┌─────────────┐
│  librarian  │        │    author    │        │    users    │
│─────────────│        │──────────────│        │─────────────│
│librarian_id │        │ author_id PK │        │ user_id  PK │
│ name        │        │ author_name  │        │ roll_no     │
│ email UNIQ  │        └──────┬───────┘        │ name        │
│ password    │               │ 1              │ batch       │
└─────────────┘               │                │ faculty     │
  (auth only)                 ▼ N              │ email UNIQ  │
                       ┌──────────────┐        └──────┬──────┘
                       │    books     │               │ 1
                       │──────────────│               │
                       │ book_id   PK │               ▼ N
                       │ book_number  │        ┌──────────────┐
                       │ title        │        │ issued_book  │
                       │ total_copies │        │──────────────│
                       │ avail_copies ◄──── N──│ issue_id  PK │
                       │ author_id FK │        │ issue_date   │
                       └──────────────┘        │ return_date  │
                                               │ status       │
                                               │ user_id   FK │
                                               │ book_id   FK │
                                               └──────────────┘
```

### 7.4 Table Summary

| Table | Primary Key | Description |
|-------|-------------|-------------|
| `librarian` | `librarian_id` SERIAL | Staff authentication — login credentials |
| `users` | `user_id` SERIAL | Registered students — the borrower entity |
| `author` | `author_id` SERIAL | Normalized author metadata |
| `books` | `book_id` SERIAL | Book catalog with live `available_copies` counter |
| `issued_book` | `issue_id` SERIAL | Borrow/return transaction records |

### 7.5 Relationships Summary

| Relationship | Cardinality | Notes |
|-------------|-------------|-------|
| `author` → `books` | 1 : N | One author can have many books in the catalog |
| `users` → `issued_book` | 1 : N | A student can have many borrow records over time |
| `books` → `issued_book` | 1 : N | A book can appear in many transactions |
| `users` ↔ `books` | M : N | Resolved through the `issued_book` join table |

### 7.6 Key Constraints

| Constraint | Table | Column | Rule |
|------------|-------|--------|------|
| UNIQUE | `librarian` | `email` | No duplicate librarian accounts |
| UNIQUE | `users` | `email` | No duplicate student registrations |
| REFERENCES | `books` | `author_id` | Must reference a valid `author` row |
| REFERENCES | `issued_book` | `user_id` | Must reference a valid `users` row |
| REFERENCES | `issued_book` | `book_id` | Must reference a valid `books` row |
| NULLABLE | `issued_book` | `return_date` | `NULL` = book not yet returned |

---

## 8. Authentication & Security

### 8.1 Librarian Authentication

LMS uses a **dedicated `librarian` table** queried directly with raw SQL. The login flow:

```python
cursor.execute(
    "SELECT librarian_id, name FROM librarian WHERE email = %s AND password = %s",
    (email, password)
)
librarian = cursor.fetchone()
if librarian:
    request.session['librarian_id'] = librarian[0]
    request.session['librarian_name'] = librarian[1]
```

On success, the librarian's ID and name are stored in Django's server-side session. On logout, the session is flushed.

### 8.2 Session-Based Route Protection

All views check for an active session at the start. If no session exists, the request is redirected to the login page:

```python
def some_view(request):
    if 'librarian_id' not in request.session:
        return redirect('login')
    # ... proceed
```

### 8.3 CSRF Protection

All POST requests are protected by Django's **CSRF middleware**. The CSRF token is embedded in every form and validated server-side before any data modification is executed.

### 8.4 Parameterized Queries

All raw SQL uses **psycopg2 parameterized queries** (`%s` placeholders) — never string formatting. This completely prevents SQL injection:

```python
# Safe — psycopg2 escapes the values
cursor.execute("SELECT * FROM users WHERE roll_no = %s", (roll_no,))

#  Never done — vulnerable to SQL injection
cursor.execute(f"SELECT * FROM users WHERE roll_no = '{roll_no}'")
```

### 8.5 Security Measures Summary

| Concern | Implementation |
|---------|---------------|
| Authentication | Raw SQL query on `librarian` table — `WHERE email=%s AND password=%s` |
| Session Management | Django server-side sessions — `request.session` |
| Route Protection | Manual session check at the top of every view |
| CSRF Protection | Django `CsrfViewMiddleware` on all POST routes |
| SQL Injection | psycopg2 parameterized queries (`%s`) throughout |
| Duplicate Accounts | `UNIQUE` on `librarian.email` and `users.email` enforced by PostgreSQL |

---

## 9. Key Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Librarian Login** | Raw SQL auth against `librarian` table — session stored server-side |
| 2 | **Live Dashboard** | Three `COUNT(*)` queries — Total Books, Total Students, Issued Books |
| 3 | **Author Management** | `INSERT INTO author` — normalized, separate from books |
| 4 | **Book Catalog** | `INSERT INTO books` with `book_number`, title, copies, `author_id` FK |
| 5 | **Student Registry** | `INSERT INTO users` with roll_no, batch, faculty, email |
| 6 | **Book Issuance** | `INSERT INTO issued_book` + `UPDATE books SET available_copies - 1` |
| 7 | **Book Returns** | `UPDATE issued_book SET return_date, status` + `available_copies + 1` |
| 8 | **Availability Enforcement** | `WHERE available_copies > 0` check before every issue |
| 9 | **Transaction Audit Trail** | `issued_book` rows are never deleted — permanent borrow history |
| 10 | **Search** | `SELECT ... WHERE book_number = %s` and `WHERE roll_no = %s` |

---

## 10. Module Descriptions

### 10.1 Authentication Module

Queries the `librarian` table with a raw `SELECT`. Stores result in `request.session`. Logout calls `request.session.flush()`.

```python
# Login
cursor.execute(
    "SELECT librarian_id, name FROM librarian WHERE email=%s AND password=%s",
    (email, password)
)

# Logout
request.session.flush()
```

---

### 10.2 Dashboard Module

Three independent `COUNT(*)` queries executed on page load:

```sql
SELECT COUNT(*) FROM books;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM issued_book WHERE status = 'issued';
```

Results returned as JSON → rendered into the three stat cards by JavaScript.

---

### 10.3 Author Management Module

Inserts a new row into the normalized `author` table. Authors must exist before a book referencing them can be added.

```sql
INSERT INTO author (author_name) VALUES (%s);
SELECT author_id, author_name FROM author ORDER BY author_id;
```

---

### 10.4 Book Management Module

Inserts books with a JOIN-friendly `author_id`. Search queries use `book_number`:

```sql
-- Add book
INSERT INTO books (book_number, title, total_copies, available_copies, author_id)
VALUES (%s, %s, %s, %s, %s);

-- Search
SELECT b.book_id, b.book_number, b.title, a.author_name,
       b.total_copies, b.available_copies
FROM books b
JOIN author a ON b.author_id = a.author_id
WHERE b.book_number = %s;
```

---

### 10.5 Student Management Module

Inserts student records and searches by `roll_no`:

```sql
-- Add student
INSERT INTO users (roll_no, name, batch, faculty, email)
VALUES (%s, %s, %s, %s, %s);

-- Search
SELECT user_id, roll_no, name, batch, faculty, email
FROM users
WHERE roll_no = %s;
```

---

### 10.6 Issue / Return Transaction Module

The core module. All operations are explicit `INSERT` and `UPDATE` statements executed in sequence:

```sql
-- ISSUE: Step 1 — check availability
SELECT available_copies FROM books WHERE book_id = %s;

-- ISSUE: Step 2 — create transaction record
INSERT INTO issued_book (issue_date, status, user_id, book_id)
VALUES (%s, 'issued', %s, %s);

-- ISSUE: Step 3 — decrement counter
UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s;

---

-- RETURN: Step 1 — find the active transaction
SELECT issue_id FROM issued_book
WHERE user_id = %s AND book_id = %s AND status = 'issued';

-- RETURN: Step 2 — close the transaction
UPDATE issued_book
SET return_date = %s, status = 'returned'
WHERE issue_id = %s;

-- RETURN: Step 3 — restore availability
UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s;
```
---
### Screenshorts
### Login Page
<img width="2294" height="1137" alt="Screenshot 2026-02-21 213119" src="https://github.com/user-attachments/assets/32c7df09-3f39-49c7-82e7-555de0de9878" />

### Dashboard
<img width="2530" height="1199" alt="Screenshot 2026-02-21 213139" src="https://github.com/user-attachments/assets/181be733-7771-4a81-9510-d859227fff59" />

### Book Management
<img width="2341" height="1168" alt="Screenshot 2026-02-21 213156" src="https://github.com/user-attachments/assets/dc3cd325-5faf-4d7d-bf15-d26fb2356230" />

### Student Management

<img width="2492" height="1164" alt="Screenshot 2026-02-21 213216" src="https://github.com/user-attachments/assets/88024d88-5961-46a6-80fb-abc3c8aac152" />

### Issue/ Return 
<img width="2490" height="1178" alt="Screenshot 2026-02-21 213234" src="https://github.com/user-attachments/assets/bf8dd2bb-4e5d-4c6c-a382-c55d1cdf1ed1" />

---

## 11. Pages & Routes

| Page | Route | Auth | Description |
|------|-------|------|-------------|
| Login | `/` | No | Librarian login — system entry point |
| Dashboard | `/dashboard/` | Yes | Live stats via `COUNT(*)` queries |
| Books | `/books/` | Yes | Add books (with author), search catalog |
| Students | `/students/` | Yes | Register and search students |
| Issue / Return | `/transactions/` | Yes | Issue and return books |
| Admin | `/admin/` | Superuser | Django Admin panel |

---

## 12. Project Structure

```
library-management-system/
│
├── backend/                              # Django project root
│   ├── settings.py                       # DB config — PostgreSQL via psycopg2
│   ├── urls.py                           # Root URL routing
│   ├── wsgi.py                           # WSGI entry point
│   │
│   └── library/                          # Core Django application
│       ├── __init__.py
│       ├── admin.py                      # Django Admin (optional superuser panel)
│       ├── views.py                      # All views — raw SQL via psycopg2 cursors
│       ├── urls.py                       # App-level URL routing
│       └── db.py                         # psycopg2 connection helper
│
├── staticfiles/                          # Frontend static assets
│   ├── librarySystem.html                # Main SPA — all UI sections in one file
│   ├── librarySystemStyle.css            # Sidebar, cards, forms, layout
│   └── librarySystem.js                  # Client-side navigation, fetch, DOM updates
│
├── library.sql                           # Full PostgreSQL schema (source of truth)
├── manage.py                             # Django management utility
├── requirements.txt                      # pip dependencies (django, psycopg2)
└── README.md                             # This file
```

### Key Files

| File | Purpose |
|------|---------|
| `views.py` | All view functions — every DB call is a raw SQL string via psycopg2 cursor |
| `db.py` | Central psycopg2 connection helper — `get_connection()` used by all views |
| `library.sql` | The complete schema — five `CREATE TABLE` statements, one seed `INSERT` |
| `librarySystem.html` | Single HTML file with all page sections, toggled by JS |
| `librarySystem.js` | Sidebar navigation, fetch API calls, dynamic DOM rendering |
| `librarySystemStyle.css` | Full stylesheet — dark sidebar, stat cards, form layouts |

---

## 13. Installation & Setup

### Prerequisites

- Python >= 3.8
- PostgreSQL >= 15
- pip & Git

### Step 1 — Clone & Environment

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
# requirements.txt contains: django, psycopg2-binary
```

### Step 2 — Database Setup

```bash
# Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE lms;"

# Apply the schema (creates all 5 tables + seeds default librarian)
psql -U postgres -d lms < library.sql
```

### Step 3 — Configure Database Connection

Update the psycopg2 connection in `library/db.py`:

```python
import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="lms",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    )
```

### Step 4 — Run the Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** and log in with the default librarian account:

```
Email:    admin@gmail.com
Password: admin1234
```

> ⚠️ Change the default password immediately in production.

---

## 14. Environment Variables

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (used in db.py)
DB_NAME=lms
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

> ⚠️ **Never commit `.env` to Git.** Add it to `.gitignore` before your first push.

---

## 15. Team Members & Contributions

| Name | Role | Key Contributions |
|------|------|-------------------|
| **Arun Raj Neupane** | Frontend Developer | UI/UX design, HTML/CSS/JS implementation, responsive sidebar layout, all page screens (Login, Dashboard, Books, Students, Issue/Return), JavaScript navigation engine, fetch API integration |
| **Naresh Rasaili** | Backend Developer | Django project setup, URL routing, all view functions, raw SQL query writing for auth/book/author/student modules, session management, psycopg2 integration |
| **Bipin Tharu** | Backend Developer | Full PostgreSQL schema design (`library.sql`), `issued_book` transaction query logic, `available_copies` enforcement via `UPDATE` statements, FK constraint design, parameterized query safety, audit trail implementation |

---

<div align="center">

**Academic Project — Library Management System — 2026**

*Built with Django · psycopg2 · PostgreSQL · HTML / CSS / JavaScript*

</div>
