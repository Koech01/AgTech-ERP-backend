# AgTech ERP Setup Guide
AgTech ERP platform built with Django and PostgreSQL. It enables Admin users to manage farmers and their crops, while Farmers can manage their own profiles and crops. The backend exposes a RESTful API with role-based access control (RBAC).


# Table of Contents
    - Overview
    - Prerequisites
    - Installation
    - Environment Setup
    - PostgreSQL Setup  
    - Create Django Admin & Demo Farmer Accounts
    - Running the Backend 
    - Demo Credentials 


# Overview
    - Backend Framework: Django 5.x
    - Authentication: JWT (via Django REST Framework SimpleJWT)
    - Database: PostgreSQL


# Prerequisites
Before you begin, ensure you have the following installed:
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) (3.x)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [PostgreSQL](https://www.postgresql.org/download/)


# Installation
Clone the repository and set up your virtual environment:

1. Clone the repository:
```bash
git clone https://github.com/Koech01/AgTech-ERP-backend
virtualenv AgTech-ERP-backend/
cd AgTech-ERP-backend
```

2. Install dependencies:
```bash
source bin/activate
pip install -r requirements.txt
```

# Environment Setup.
Configure the environment:

1. Create an .env file:
```bash
touch .env 
```

2. Generate a Django secret key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

3. Open the `.env` file and add the following lines, with your newly generated secret key for `SECRET_KEY`. Make sure to keep DEBUG=True for local development:
```env
SECRET_KEY=your_generated_secret_key_here
DEBUG=True

# Database Configuration
DB_NAME=agritech_db
DB_USER=admin
DB_PASSWORD=Admin@123
DB_HOST=127.0.0.1
DB_PORT=5432
```

# PostgreSQL Setup.
Set up the PostgreSQL database and user for Django:

1. Make migrations for the  **users** app:
```bash
python manage.py makemigrations users
python manage.py migrate users
```

1. Start the PostgreSQL service:
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql 
```

2. Access the PostgreSQL shell:
```bash
sudo -u postgres psql
```

3. Create a database and a user:
```env
CREATE DATABASE agritech_db;
CREATE USER admin WITH PASSWORD 'Admin@123';
GRANT ALL PRIVILEGES ON DATABASE agritech_db TO admin;
```

4. Grant schema and table privileges:
```env
\c agritech_db   -- connect to your database

-- Give admin full privileges on the public schema
GRANT ALL PRIVILEGES ON SCHEMA public TO admin;

-- Allow admin to create tables, sequences, and functions by default
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO admin;

\q   
```

# Create Django Admin & Demo Farmer Accounts.
Set up the PostgreSQL database and user for Django:
 
1. Creating superuser (Admin):
The admin account is **pre-seeded** and can be created using the following command:

```bash
python manage.py createadmin
```

2. Seed demo farmer account (Koech) via Django shell:
```bash
python manage.py shell
```

```bash
from users.models import User   

# Create Farmer user
farmer = User.objects.create_user(
    username='koech',
    email='koech@agritech.com',
    password='Koech@123',
    role=User.Role.FARMER  
)

farmer.save()   
 
exit()
```

You can now access the application at `http://127.0.0.1:8000/`.
 
# Demo Credentials
  - Link   : [Ag Tech ERP](https://ag-tech-erp-frontend-deploy.vercel.app/)
  - Admin  : email - admin@agritech.com | password - Admin@123
  - Farmer : email - koech@agritech.com | password - Koech@123
