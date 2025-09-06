from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from events.models import Event


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(student=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})    

@login_required
def book_now(request, id):
    event = get_object_or_404(Event, id=id)
    
    # Check if user already has a booking for this event
    existing_booking = Booking.objects.filter(student=request.user, event=event).first()
    if existing_booking.status == 'confirmed':
        messages.warning(request, f"You already have a booking for {event.title}")
        return redirect('event_detail', id=event.id)
    elif existing_booking.status == 'cancelled':
        messages.warning(request, f"You already have a cancelled booking for {event.title}")
        existing_booking.status = 'confirmed'
        existing_booking.save()
        return redirect('event_detail', id=event.id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, event=event)
        if form.is_valid():
            # Create the booking
            booking = form.save(commit=False)
            booking.student = request.user
            booking.event = event
            booking.save()
            
            # Update available seats
            event.seats -= form.cleaned_data['number_of_seats']
            event.save()
            
            messages.success(request, f"Successfully booked 1 seat for {event.title}")
            return redirect('event_list')
    else:
        form = BookingForm(event=event)
    
    return render(request, 'bookings/booking.html', {
        'event': event,
        'form': form
    })

@login_required
def confirm_booking(request, id):
    event = get_object_or_404(Event, id=id)
    booking = get_object_or_404(Booking, student=request.user, event=event)
    
    return render(request, 'bookings/booking_confirmation.html', {
        'event': event,
        'booking': booking
    })

@login_required
def cancel_booking(request, id):  
    booking = get_object_or_404(Booking, id=id)

    # restore seats to the event
    event = booking.event
    event.seats += booking.number_of_seats if booking.number_of_seats else 1
    event.save()
    booking.status = 'cancelled'
    booking.save()

    # delete booking

    return redirect("bookings")  # make sure you have a 'bookings' url name


