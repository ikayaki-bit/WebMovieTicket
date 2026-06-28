from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie-list'),
    path('seats/', views.seat_map, name='seat-map'),
    path('booking/create/', views.create_booking, name='create-booking'),
]