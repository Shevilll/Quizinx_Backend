# Quiz Application

This is a full-stack quiz application with a Django backend and React frontend. The backend handles quiz data and scoring, while the frontend provides a user-friendly interface to interact with the quizzes.

## Table of Contents

-   [Backend Setup (Django)](#backend-setup-django)
-   [Frontend Setup (React)](#frontend-setup-react)
-   [API Endpoints](#api-endpoints)
-   [Deployment](#deployment)

---

## Backend Setup (Django)

### Prerequisites

-   Python 3.8+
-   Django 3.x+
-   Gunicorn (for production)
-   PostgreSQL (or any other preferred database)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Shevilll/Quizinx_Backend
    cd Quizinx_Backend
    ```

2. Set up a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For macOS/Linux
    venv\Scripts\activate     # For Windows
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```
