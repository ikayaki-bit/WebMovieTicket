# Movie Ticket Booking System

## Project Outline
This web application is a single-page system designed for booking movie tickets. It features real-time seat availability management and an interactive layout to prevent overlapping or duplicate bookings.

### Core Functionalities
- **Asynchronous Interactions:** Powered by HTMX to provide seamless, dynamic UI updates without full page reloads.
- **Dynamic Filtering:** Selecting a movie and a date instantly filters the available showtimes and show options.
- **Interactive Seat Map:** Displays vacant seats (clickable) and already-booked seats (grayed out and unclickable).
- **Profile Auto-fill:** Automatically verifies user login status to pre-fill user profiles and names during confirmation.

## Architecture & Data Layer
- **Presentation Layer:** HTML / CSS + HTMX
- **Application Layer:** Django Server (Python Views & Django ORM)
- **Data Layer:** Relational Database Storage consisting of 5 interconnected tables implemented in `FirstApp/models.py`.

## Database Schema

### 1. User Model
Manages account details for registered users.
- `id` (Auto-generated Primary Key)
- `username` (CharField, max_length=50): Unique login name.
- `password` (CharField, max_length=255): Password text.

### 2. Movie Model
Contains details of available movies.
- `id` (Auto-generated Primary Key)
- `title` (CharField, max_length=100): Title of the movie.
- `duration` (IntegerField): Runtime of the movie in minutes.

### 3. Showtime Model
Manages specific screening schedules.
- `id` (Auto-generated Primary Key)
- `movie` (ForeignKey to Movie): Cascades on delete.
- `start_time` (DateTimeField): The screening date and time.

### 4. Seat Model
Represents physical seats in the cinema hall.
- `id` (Auto-generated Primary Key)
- `seat_number` (CharField, max_length=10): Label of the seat (e.g., A-1).

### 5. Booking Model
Connects users, showtimes, and seats to process reservations.
- `id` (Auto-generated Primary Key)
- `showtime` (ForeignKey to Showtime): Cascades on delete.
- `seat` (ForeignKey to Seat): Cascades on delete.
- `user` (ForeignKey to User): Cascades on delete.

## Development Environment
- **Language:** Python >= 3.11
- **Package Manager:** `uv`
- **Virtual Environment:** `uv venv` (`.venv/`)

## Development Tools
- **Linter & Formatter:** [Ruff](https://github.com/astral-sh/ruff) (Configured for linting and code formatting)
- **Coverage Tool:** `coverage` (Used for measuring code coverage during testing)

## Setup Instructions
1. Clone this repository to your local machine.
2. Initialize the environment and sync dependencies by running:
   ```bash
   uv venv
   .venv\Scripts\Activate.ps1
   uv sync
   ```

## Testing (`tests.py`)
The test suite (`tests.py`) is fully completed. To run the tests and measure code coverage in your development environment:
```bash
# Run Django tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Production & Deployment

### 1. Deployment Decisions
- **Hosting Service:** **Render.com** (recommended cloud hosting platform for Python/Django web services).
- **Application Server:** **Gunicorn** (a robust WSGI application server designed to handle production traffic).
- **Static Files Handling:** **WhiteNoise** (enables the Django app to serve its own static files efficiently without requiring a separate Nginx or cloud storage setup).
- **Uploaded Files/Images:** The current architecture relies entirely on relational database models (Users, Movies, Showtimes, Seats, Bookings). If future updates require user-uploaded files, they will be routed to a cloud object storage service (such as AWS S3 or Cloudinary).

### 2. Configuration Settings (`settings.py`)
Ensure your production settings include:
- `DEBUG = False`
- `ALLOWED_HOSTS = ['your-app-name.onrender.com']`
- Add `whitenoise.middleware.WhiteNoiseMiddleware` right below Django's `SecurityMiddleware`.
- Set `STATIC_ROOT = BASE_DIR / 'staticfiles'` and configure `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`.

### 3. Procfile Configuration
Create a `Procfile` in the root directory of your repository with the following entry:
```text
web: gunicorn myproject.wsgi --log-file -
```

### 4. Deploying to Render.com
1. Push your repository to GitHub.
2. Log in to [Render](https://render.com/), create a new **Web Service**, and connect your GitHub repository.
3. Configure the build and start parameters:
   - **Environment:** `Python 3`
   - **Build Command:** `uv pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn myproject.wsgi:application`
4. Add your production environment variables in the Render dashboard (e.g., `DJANGO_SECRET_KEY`, `DEBUG=False`).
5. Trigger the deployment. Once built, run database migrations in the Render shell using:
   ```bash
   python manage.py migrate
   ```