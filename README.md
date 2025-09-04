# AgTech ERP Setup Guide
AgTech ERP platform built with Django and PostgreSQL. It enables Admin users to manage farmers and their crops, while Farmers can manage their own profiles and crops. The backend exposes a RESTful API with role-based access control (RBAC).


# Table of Contents
    - Overview
    - Tech Stack
    - Prerequisites
    - Installation
    - Environment Setup 
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
```
You can now access the application at `http://127.0.0.1:8000/`.

# Demo Credentials
    - Admin  : email-admin@agritech.com  | password-Admin@123
    - Farmer : koech@agritech.com  | Koech@123