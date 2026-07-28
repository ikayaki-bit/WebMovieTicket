from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# 1. Main Home Page (Single-page interface)
def home(request):
    """Render the main single-page interface for the booking system."""
    mock_movies = [
        {"movie_id": 1, "title": "Inception", "duration": 148},
        {"movie_id": 2, "title": "Interstellar", "duration": 169},
        {"movie_id": 3, "title": "The Dark Knight", "duration": 152},
    ]
    context = {
        'movies': mock_movies,
    }
    return render(request, 'FirstApp/home.html', context)

# 2. Step 1: Get Movies & Dates (Mock List)
def movie_list(request):
    """Return a mock list of movies and available dates based on user selection."""
    selected_movie = request.GET.get('movie')
    selected_date = request.GET.get('date')

    # data based on the Movies Table specification
    mock_movies = [
        {"movie_id": 1, "title": "Inception", "duration": 148},
        {"movie_id": 2, "title": "Interstellar", "duration": 169},
        {"movie_id": 3, "title": "The Dark Knight", "duration": 152},
    ]

    matched_movies = None
    if selected_movie:
        for movie in mock_movies:
            if movie['movie_id'] == int(selected_movie):
                matched_movies = movie
                break

    """Context dictionary to pass selected movie and date to the template if needed."""
    context = {
        'movies': mock_movies,
        'selected_movie': matched_movies,
        'selected_date': selected_date,
    }

    """Return the HTML for the result section"""
    if request.headers.get('HX-Request'):
        if matched_movies:
            html = f"""
                <h3>Selected Movie Results:</h3>
                <p>Movie Title: {matched_movies['title']}</p>
                <p>Duration: {matched_movies['duration']} minutes</p>
                <p>Date: {selected_date}</p>
            """
        else:
            html = "<p>Please select a movie.</p>"
        return HttpResponse(html)

    return render(request, 'FirstApp/home.html', context)

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