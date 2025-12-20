# PermitPro - Permit Request Management System

A Django-based web application for managing trucking permit requests. Customers can create accounts, manage their company information, fleet (trucks/trailers), drivers, and submit permit requests. Employees can review submissions, manage permits, and email customers with file attachments.

## Features

### Customer Portal
- **User Registration & Authentication** - Secure private accounts for customers
- **Company Management** - Store and update company info (USDOT, FEIN, IFTA, etc.)
- **Fleet Management** - Add/edit trucks and trailers with axle configurations
- **Driver Management** - Maintain driver list with license information
- **Permit Requests** - Submit permit applications with:
  - Load descriptions and dimensions
  - State selection with travel dates
  - Equipment assignment (trucks, trailers, drivers)
  - Payment method selection
- **Document Management** - Upload vehicle registration PDFs

### Employee Dashboard
- **Permit Review** - View and manage all permit submissions
- **Status Management** - Update permit status (Pending, In Progress, Completed, etc.)
- **Assignment** - Assign permits to employees
- **Email System** - Send emails to customers with drag-and-drop file attachments
- **Company Directory** - Browse all registered companies
- **Comment System** - Internal and customer-visible comments

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Clone and navigate to project:**
```bash
cd permit_system
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py makemigrations accounts company fleet permits dashboard
python manage.py migrate
```

5. **Create superuser (admin):**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

7. **Access the application:**
- Customer Portal: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Creating Test Users

### Create an Employee User
After creating a superuser, go to the admin panel and:
1. Navigate to Accounts > Users
2. Edit your superuser or create a new user
3. Set `user_type` to "Employee" or "Admin"

### Create a Customer Account
Simply register through the registration form at `/accounts/register/`

## Project Structure

```
permit_system/
├── accounts/          # User authentication & profiles
├── company/           # Company management
├── fleet/             # Vehicle & driver management
├── permits/           # Permit request handling
├── dashboard/         # Dashboard views & email system
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploads
└── permit_system/     # Project settings
```

## Email Configuration

For production, configure email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'permits@yourdomain.com'
```

## Technology Stack

- **Backend:** Django 4.2
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** Bootstrap 5, vanilla JavaScript
- **Styling:** Custom CSS with CSS variables
- **Icons:** Bootstrap Icons

## License

MIT License

