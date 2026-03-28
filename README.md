# FastAPI – User Management API with Authentication & Session Control

## Project Overview

This project is a **FastAPI-based backend application** that provides:

* User Registration & Login 
* JWT Authentication 
* Single Device Session Control (Advanced Security) 
* User CRUD Operations 
* Text Analysis Feature 
* MySQL Database Integration 

---

## Tech Stack

* **Backend Framework:** FastAPI
* **Database:** MySQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT (python-jose)
* **Password Hashing:** Passlib (bcrypt)
* **Server:** Uvicorn

---

## Project Structure

```
app/
│── main.py
│── database.py
│
├── core/
│   ├── config.py
│   └── security.py
│
├── models/
│   ├── user.py
│   └── analysis.py
│
├── schemas/
│   └── user.py
│
├── routes/
│   ├── auth_routes.py
│   └── protected_routes.py
│
└── auth.py
```

---

## Installation & Setup

### 1️Clone Repository

```bash
git clone https://github.com/ZiaAhmadAyoob/User-Management-API-with-Authentication-Session-Control.git
cd User-Management-API-with-Authentication-Session-Control
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=fastapi_task5
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5️⃣ Run Server

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

After running server, open:

 http://127.0.0.1:8000/docs

---

## Authentication Flow

1. Register user
2. Login → get JWT token
3. Use token in protected routes

---

## Single Device Login (Session Control)

### How it works:

* On login:

  * A new `session_id` is generated
  * Stored in database
  * Included in JWT

* On every request:

  * Token is decoded
  * `session_id` is verified

### If user logs in from another device:

* Old session becomes invalid
* API returns:

```
401 Unauthorized – Session expired due to login from another device
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description   |
| ------ | -------- | ------------- |
| POST   | `/login` | User login    |
| POST   | `/users` | Register user |

---

### Users

| Method | Endpoint      | Description     |
| ------ | ------------- | --------------- |
| GET    | `/users`      | Get all users   |
| GET    | `/users/{id}` | Get user detail |
| DELETE | `/users/{id}` | Delete user     |

---

### Analysis

| Method | Endpoint                             | Description      |
| ------ | ------------------------------------ | ---------------- |
| POST   | `/users/{id}/analysis`               | Create analysis  |
| GET    | `/users/{id}/analysis`               | Get all analyses |
| GET    | `/users/{id}/analysis/{analysis_id}` | Get one analysis |
| DELETE | `/users/{id}/analysis/{analysis_id}` | Delete analysis  |

---

## Features

✔ JWT Authentication
✔ Password Hashing (bcrypt)
✔ MySQL Database Integration
✔ SQLAlchemy ORM
✔ Pagination & Filtering
✔ Secure API Endpoints
✔ Single Active Session per User

---

## Important Notes

* MySQL requires `VARCHAR(length)` → Always define length in models
* Database must exist before running app
* Do NOT expose `.env` file

---

## Future Improvements

* Add Refresh Tokens
* Role-Based Access Control (RBAC)
* Docker Support
* Deployment (AWS / Render)

---

## Author

**ZIA AHMAD AYOOB**

---

## Support

If you like this project, give it a ⭐ on GitHub!