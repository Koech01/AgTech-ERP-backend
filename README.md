# AgTech ERP Setup Guide
AgTech ERP platform built with Django and PostgreSQL. It enables Admin users to manage farmers and their crops, while Farmers can manage their own profiles and crops. The backend exposes a RESTful API with role-based access control (RBAC).

# Table of Contents
    - Overview
    - Tech Stack
    - Prerequisites
    - Installation
    - Environment Setup
    - Database Migrations
    - Running the Backend
    - API Endpoints
    - Demo Credentials
    - License


Overview

Backend features:

Authentication & Authorization

JWT-based login/signup

Role-based access: Admin vs Farmer

Admin Role

Dashboard stats: total farmers, total crops, crops per farmer

Farmer management: view, add, edit, delete farmers

Crop management: view, edit, delete any crop

Farmer Role

Dashboard stats: total crops, crops by type, rank among other farmers

Profile management: view/update profile and profile icon

Crop management: add, view, edit, delete only own crops




Tech Stack

Backend Framework: Django 5.x

Authentication: JWT (via Django REST Framework SimpleJWT)

Database: PostgreSQL

Caching / Chat Support: Redis (for WebSocket chat)

API Documentation: Django REST Framework



Prerequisites

Before starting, ensure you have:

Git

Python 3.x

virtualenv

Docker
 (for Redis)
PostgreSQL installed and running


# Prerequisites
Before you begin, ensure you have the following installed:
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) (3.x)
- [Node.js](https://nodejs.org/en/download)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [Docker](https://docs.docker.com/engine/install/)

# Installation
Clone the repository and set up your virtual environment:

1. Clone the repository:
```bash
git clone https://github.com/Koech01/veg-connect.git
virtualenv veg-connect/
cd veg-connect
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
```

# Frontend Setup.

1. Set up the frontend by navigating to the frontend directory and installing dependencies:
```bash
cd frontend
npm install
npm run build
cd ..
```

# Running the Application.

1. For chat functionality, ensure Redis is running:
```bash
sudo docker run -d -p 6379:6379 redis 
```
Enter your password.

2. Start the Django development server:
```bash
python manage.py runserver 
```
You can now access the application at `http://127.0.0.1:8000/`.

# License.
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
