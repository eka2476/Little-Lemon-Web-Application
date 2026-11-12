Little Lemon Back-End Developer Capstone
=====================================

This project contains a Django website, MySQL-backed Menu and Booking models,
Django REST Framework CRUD endpoints, Djoser user registration and token login,
and unit tests.

API paths for peer review (run server at http://127.0.0.1:8000):
GET    /api/menu-items/
POST   /api/menu-items/
GET    /api/menu-items/<id>/
PUT    /api/menu-items/<id>/
DELETE /api/menu-items/<id>/
GET    /api/bookings/
GET    /api/bookings/?date=2026-11-12
POST   /api/bookings/
GET    /api/bookings/<id>/
PUT    /api/bookings/<id>/
DELETE /api/bookings/<id>/
POST   /auth/users/             (register: username, password)
POST   /auth/token/login/       (username, password -> auth_token)
POST   /auth/token/logout/
GET    /admin/
GET    /book/
GET    /reservations/

API GET endpoints are public. API POST, PUT, PATCH and DELETE require a token.
In Insomnia: Auth -> API Key or Header: Authorization: Token <auth_token>
For JSON requests: Content-Type: application/json

SETUP
1. Install Python 3.11, pipenv and MySQL.
2. cd littlelemon
3. pipenv install
4. Create a MySQL database named reservations:
   CREATE DATABASE reservations CHARACTER SET utf8mb4;
5. Configure MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST and
   MYSQL_PORT environment variables for your own local MySQL credentials.
6. pipenv run python manage.py migrate
7. pipenv run python manage.py createsuperuser
8. pipenv run python manage.py test
9. pipenv run python manage.py runserver

For the HTML booking form, use /book/. It uses the original public form endpoint
/bookings (GET/POST), while the DRF API uses /api/bookings/.

To submit: create a GitHub repository, commit all project source files,
push the repository, and paste the GitHub repository URL into Coursera.
Never commit local credentials, database files or virtual environments.
