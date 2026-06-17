# Movie Ticket Booking System

## Project Outline
[cite_start]This web application is a single-page system designed for booking movie tickets[cite: 58, 74]. [cite_start]It features real-time seat availability management and an interactive layout to prevent overlapping or duplicate bookings[cite: 22, 61].

### Core Functionalities
- [cite_start]**Asynchronous Interactions:** Powered by HTMX to provide seamless, dynamic UI updates without full page reloads[cite: 41, 42].
- [cite_start]**Dynamic Filtering:** Selecting a movie and a date instantly filters the available showtimes and show options[cite: 32, 75].
- [cite_start]**Interactive Seat Map:** Displays vacant seats (clickable) and already-booked seats (grayed out and unclickable)[cite: 34, 76].
- [cite_start]**Profile Auto-fill:** Automatically verifies user login status to pre-fill user profiles and names during confirmation[cite: 35, 36, 49].

## Architecture & Data Layer
- [cite_start]**Presentation Layer:** HTML / CSS + HTMX [cite: 40, 41]
- [cite_start]**Application Layer:** Django Server (Python Views & Django ORM) [cite: 46, 47, 50]
- [cite_start]**Data Layer:** Relational Database Storage consisting of 5 interconnected tables: `Users`, `Movies`, `Showtimes`, `Seats`, and `Bookings`[cite: 52, 53, 54].

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