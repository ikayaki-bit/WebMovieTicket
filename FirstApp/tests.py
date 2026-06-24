from django.test import TestCase
from django.utils import timezone
from .models import User, Movie, Showtime, Seat, Booking

class ModelTest(TestCase):
    def test_user_str(self):
        user = User.objects.create(username="testuser", password="password123")
        self.assertEqual(str(user), "testuser")

    def test_movie_str(self):
        movie = Movie.objects.create(title="Inception", duration=148)
        self.assertEqual(str(movie), "Inception")

    def test_showtime_str(self):
        movie = Movie.objects.create(title="Inception", duration=148)
        now = timezone.now()
        showtime = Showtime.objects.create(movie=movie, start_time=now)
        self.assertEqual(str(showtime), f"Inception - {now}")

    def test_seat_str(self):
        seat = Seat.objects.create(seat_number="A-1")
        self.assertEqual(str(seat), "A-1")

    def test_booking_str(self):
        user = User.objects.create(username="testuser", password="password123")
        movie = Movie.objects.create(title="Inception", duration=148)
        showtime = Showtime.objects.create(movie=movie, start_time=timezone.now())
        seat = Seat.objects.create(seat_number="A-1")
        booking = Booking.objects.create(showtime=showtime, seat=seat, user=user)
        self.assertEqual(str(booking), f"Booking #{booking.id} (testuser)")