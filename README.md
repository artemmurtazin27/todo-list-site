# Todo List Site

A simple task management web application built with Django. It lets you create,
update, complete and delete tasks, and organize them using tags.

## Features

- Create, update and delete tasks
- Mark tasks as completed / not completed
- Set an optional deadline for a task
- Create, update and delete tags
- Assign one or more tags to a task
- Responsive UI built with Bootstrap 4 (via `django-bootstrap4` and `django-crispy-forms`)

## Tech stack

- Python 3
- Django 5.2
- SQLite (default database)
- Bootstrap 4 / Crispy Forms for templates

## Project structure

```
config/     - Django project settings, root URL configuration, WSGI/ASGI entry points
todo/       - Main application: models, views, forms, urls, tests
templates/  - HTML templates
static/     - CSS files
```

## Getting started

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/artemmurtazin27/todo-list-site.git
cd todo-list-site
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the sample environment file and adjust it if needed:

```bash
cp .env.sample .env
```

The `.env` file supports the following variables:

| Variable        | Description                                   | Default                 |
|-----------------|------------------------------------------------|--------------------------|
| `SECRET_KEY`    | Django secret key                              | `fallback-secret-key-for-dev` |
| `DEBUG`         | Enable/disable debug mode                      | `True`                   |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts          | `127.0.0.1,localhost`    |

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. (Optional) Create a superuser to access the admin panel

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.
The Django admin panel is available at `http://127.0.0.1:8000/admin/`.

## Running tests

The project uses Django's built-in test framework. To run the test suite:

```bash
python manage.py test
```

## License

This project is for educational purposes.
