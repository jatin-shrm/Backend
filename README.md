# Backend - Django Authentication API

A Django REST API with custom user authentication, JWT tokens, and support for both email and username login.

## Features

- Custom User Model with email and username
- JWT Token Authentication
- Login with either email or username
- Automatic login after registration
- CORS support for frontend integration
- PostgreSQL database support

## Tech Stack

- Django 4.2+
- Django REST Framework
- Django REST Framework Simple JWT
- PostgreSQL
- Python 3.13+

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Backend
```

### 2. Create virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary python-decouple django-cors-headers
```

### 4. Environment Variables
Create a `.env` file in the root directory:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# Security Settings
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/token/` - Login (email/username + password)
- `POST /api/auth/token/refresh/` - Refresh token
- `GET /api/auth/me/` - Get current user info (requires authentication)

### Request/Response Examples

#### Register User
```json
POST /api/auth/register/
{
    "email": "user@example.com",
    "username": "username",
    "fullname": "Full Name",
    "password": "password123"
}

Response:
{
    "message": "User registered successfully",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "username": "username",
        "email": "user@example.com",
        "full_name": "Full Name"
    }
}
```

#### Login
```json
POST /api/auth/token/
{
    "username_field": "user@example.com",  // or username
    "password": "password123"
}

Response:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "username": "username",
        "email": "user@example.com",
        "full_name": "Full Name"
    }
}
```

## Project Structure

```
Backend/
├── Backend/                 # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── authapp/                # Authentication app
│   ├── models.py           # Custom User model
│   ├── views.py            # API views
│   ├── serializers.py      # DRF serializers
│   ├── backends.py         # Custom authentication backend
│   └── urls.py             # App URL configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 