from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# 1. Main Home Page (Single-page interface)
def home(request):
    """Render the main single-page interface for the booking system."""
    # In a real app, this will render a full HTML template.
    return HttpResponse("<h1>Welcome to Movie Ticket Booking System</h1><p>Select a movie to start.</p>")

# 2. Step 1: Get Movies & Dates (Mock List)
def movie_list(request):
    """Return a list of available movies for selection."""
    # Dummy data based on the Movies Table specification
    mock_movies = [
        {"movie_id": 1, "title": "Inception", "duration": 148},
        {"movie_id": 2, "title": "Interstellar", "duration": 169},
        {"movie_id": 3, "title": "The Dark Knight", "duration": 152},
    ]
    return JsonResponse({"movies": mock_movies})

# 3. Step 2: Interactive Seat Map (HTMX Snippet)
def seat_map(request):
    """Return a mock interactive seat map based on selected showtime."""
    # Simulate a dynamic HTML snippet for HTMX as outlined in the architecture
    html_snippet = """
    <div class='seat-map'>
        <h3>Select your seat</h3>
        <button style='background-color: green;'>Seat A1 (Vacant)</button>
        <button style='background-color: gray;' disabled>Seat A2 (Booked)</button>
    </div>
    """
    return HttpResponse(html_snippet)

# 4. Step 4: Final Booking Process
def create_booking(request):
    """Process the final ticket reservation and return status."""
    # Simulate processing the reservation (validating vacancy)
    # Then return a simple success response or redirect
    return HttpResponse("<p class='popup'>Booking Confirmed! Thank you.</p>")