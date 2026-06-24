from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return self.title

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"

class Seat(models.Model):
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return self.seat_number

class Booking(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking #{self.id} ({self.user.username})"