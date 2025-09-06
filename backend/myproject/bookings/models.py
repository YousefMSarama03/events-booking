from django.db import models
from accounts.models import User
from events.models import Event

class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'event')  # يمنع الطالب من حجز نفس الفعالية مرتين

    def __str__(self):
        return f"{self.student.username} - {self.event.title} ({self.number_of_seats} seats)"
