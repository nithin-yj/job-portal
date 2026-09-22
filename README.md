# Job Portal

A Django-based job portal where employees can search and apply for jobs, while employers can create job listings and manage applications.

The project includes authentication, role-based access control, job management, application tracking, resume upload, and email functionality.

---

## Features

- User registration and login
- Custom user model using email authentication
- Employee and Employer roles
- Role-based access control
- Employee job search and pagination
- Employer job creation and management
- Edit and delete job listings
- Apply for jobs
- Resume upload while applying
- PDF resume validation
- Resume size validation
- View and download applicant resumes
- Track application status
- Employers can update application status
- Duplicate application prevention
- Password reset functionality
- Welcome email after registration
- Django admin panel
- MySQL database
- Environment variable configuration
- Static file handling with WhiteNoise

---

## User Roles

### Employee

Employees can:

- Register and log in
- Browse available jobs
- Search for jobs
- View job details
- Apply for jobs
- Upload a resume while applying
- View their applications
- Check application status

### Employer

Employers can:

- Register and log in
- Create job listings
- View their posted jobs
- Edit their own jobs
- Delete their own jobs
- View applicants for their jobs
- View applicant resumes
- Download applicant resumes
- Update application status

---

## Tech Stack

### Backend

- Python
- Django

### Database

- MySQL
- Django ORM

### Frontend

- HTML
- CSS
- Vanilla JavaScript

No Bootstrap, Tailwind CSS, or other frontend frameworks are used.

### Other Tools

- python-dotenv
- WhiteNoise
- Gmail SMTP

---

## Project Setup

### Prerequisites

Make sure the following are installed:

- Python 3.13+
- MySQL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/nithin-yj/job-portal.git
cd job-portal
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## MySQL Setup

Create a MySQL database for the project.

Example:

```sql
CREATE DATABASE job_portal;
```

Create a MySQL user or use an existing user with permission to access the database.

The database configuration is loaded through environment variables.

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=job_portal
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=127.0.0.1
DB_PORT=3306

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

A sample environment file is provided as `.env.example`.

Do not commit the actual `.env` file to GitHub.

---

## Database Migration

Run the migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Create Superuser

Create a Django admin account:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the account.

---

## Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will normally be available at:

`http://127.0.0.1:8000/`

---

## Environment Variables Reference

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Enables or disables Django debug mode |
| `ALLOWED_HOSTS` | Hosts allowed to access the application |
| `DB_NAME` | MySQL database name |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_HOST` | MySQL host |
| `DB_PORT` | MySQL port |
| `EMAIL_HOST_USER` | Gmail account used for sending emails |
| `EMAIL_HOST_PASSWORD` | Gmail app password |

---

## Project Structure

```text
Job_portal/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── forms.py
│   ├── managers.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── jobs/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── base.html
│
├── media/
├── staticfiles/
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .env
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

`venv/`, `.env`, `db.sqlite3`, `media/`, and `staticfiles/` are ignored from Git where appropriate and are not intended to be committed as project source files.

---

## Application Structure

The project is divided into two main Django applications.

### Accounts

The `accounts` application handles:

- User registration
- Login
- Logout
- Password reset
- Custom user model
- User roles
- Authentication-related forms
- Role-based access control

### Jobs

The `jobs` application handles:

- Job creation
- Job listing
- Job search
- Job details
- Job editing
- Job deletion
- Job applications
- Application status
- Resume upload
- Resume viewing and downloading

---

## Database Design

### User

The project uses a custom Django user model.

Users authenticate using their email address instead of a username.

Each user has a role:

```text
EMPLOYEE
EMPLOYER
```

### Job

A job belongs to an employer.

Important fields include:

- Employer
- Title
- Description
- Location
- Salary
- Created date
- Updated date
- Active status

### Application

An application connects an employee with a job.

Important fields include:

- Employee
- Job
- Resume
- Application status
- Applied date

Application statuses include:

```text
APPLIED
SELECTED
REJECTED
```

A database constraint prevents the same employee from applying to the same job more than once.

---

## Resume Handling

Employees can upload their resume when applying for a job.

The application validates:

- File extension
- Actual PDF file content
- File size

Only PDF resumes are accepted and the maximum file size is **5 MB**.

Resumes are not exposed through a public media URL.

Employers can access resumes through protected Django views only when they are authorized to view the corresponding application's job.

Employers can:

- View a resume in the browser
- Download a resume

An employer cannot access resumes belonging to another employer's job.

---

## Authentication and Authorization

The project uses Django's authentication system.

Authentication is required for protected pages.

Role-based access is implemented using a custom decorator.

For example:

```python
@role_required(User.Role.EMPLOYER)
```

This ensures that only users with the required role can access specific views.

Object ownership is also checked when employers manage jobs and applications.

For example, an employer can only edit or delete jobs that belong to that employer.

---

## Security

Several security measures are implemented in the project.

### CSRF Protection

POST forms include Django CSRF protection.

```html
{% csrf_token %}
```

### Password Security

Passwords are handled using Django's password hashing system.

### Role-Based Authorization

Employees cannot access employer-only functionality, and employers cannot access employee-only functionality.

### Object-Level Authorization

Users cannot access or modify another user's jobs or applications by changing an ID in the URL.

### Resume Protection

Resume files are served through authenticated and authorized Django views rather than being publicly exposed.

### Environment Variables

Sensitive configuration such as:

- Django secret key
- Database password
- Email credentials

is stored in `.env` instead of being hard-coded in the source code.

### SQL Injection Protection

The project uses Django ORM queries rather than manually constructing raw SQL queries for application functionality.

---

## Application Flow

### Employee Flow

```text
Register
   ↓
Login
   ↓
Browse Jobs
   ↓
Search / View Job
   ↓
Apply
   ↓
Upload Resume
   ↓
Application Created
   ↓
Track Application Status
```

### Employer Flow

```text
Register
   ↓
Login
   ↓
Employer Dashboard
   ↓
Create Job
   ↓
Manage Jobs
   ↓
View Applicants
   ↓
View / Download Resume
   ↓
Update Application Status
```

---

## Email

The project uses Gmail SMTP for sending emails.

For example, a welcome email can be sent after successful user registration.

Gmail App Passwords should be used instead of a normal Gmail account password when configuring SMTP authentication.

---

## Static Files

Static CSS files are stored inside:

```text
static/
```

WhiteNoise is configured to handle static files, including production static file collection.

To collect static files:

```bash
python manage.py collectstatic
```

---

## Django Admin

The Django admin panel can be accessed at:

`/admin/`

Use the superuser account created with:

```bash
python manage.py createsuperuser
```

The admin panel can be used to inspect and manage application data.

---

## Common Django Commands

Start the development server:

```bash
python manage.py runserver
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Collect static files:

```bash
python manage.py collectstatic
```

Run Django checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

---

## Development Notes

The project follows Django's standard application structure with separate apps for authentication and job-related functionality.

The frontend uses server-rendered Django templates with HTML and vanilla CSS rather than a frontend framework.

Django ORM is used for database operations.

The project is designed around role-based workflows so that employees and employers have different permissions and functionality.

---

## Future Improvements

Possible improvements include:

- Job recommendations
- Advanced job filtering
- Employer profile management
- Employee profile management
- Saved jobs
- Application withdrawal
- Email notifications when application status changes
- Automated tests for more application flows
- Production deployment with private object storage for resumes
- Improved dashboard analytics

---

## Developer

**Nithin YJ**

B.E. Computer Science and Engineering — 2026

GitHub:  
https://github.com/nithin-yj/job-portal

---

## License

This project is intended as a personal portfolio and learning project.
