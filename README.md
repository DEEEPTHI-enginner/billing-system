# Billing System - FastAPI + PostgreSQL

## Features
- Dynamic billing form
- Denomination handling
- Greedy balance calculation
- Async email invoice sending
- Purchase history view

## Tech Stack
- FastAPI
- SQLAlchemy
- PostgreSQL
- Jinja2

## Setup Instructions

step 1: Clone repo

1. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

2. Install dependencies
   pip install -r requirements.txt

3. Create PostgreSQL DB
   CREATE DATABASE billing_db;

4. Update .env file

5. Add your Gmail SMTP credentials

6. Enable App Password in Gmail

7. Run server
   uvicorn app.main:app --reload

8. Open
   http://127.0.0.1:8000

## Assumptions
- Tax applied per product
- Greedy denomination logic
- Stock reduces after successful invoice