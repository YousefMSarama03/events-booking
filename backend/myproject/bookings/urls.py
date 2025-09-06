from django.urls import path
from . import views


urlpatterns = [
    path('bookings', views.my_bookings ,name= 'bookings'),
    path('bookings/<int:id>/', views.book_now, name='book_now'),
    path('bookings/<int:id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('booking/<int:id>/cancel/',views.cancel_booking,name='cancel_booking')
]
