from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime
# Create your views here.

def home(request):
    events = Event.objects.all()
    return render(request, 'events/home.html',{'events':events})


@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/events.html',{'events': events})

@login_required
def event_detail(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'events/event_details.html', {'event': event})


@login_required
def manage_events(request):
    # Check if user is admin
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('event_list')
    
    if request.method == 'POST':
        # Handle event creation
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        seats = request.POST.get('seats')
        
        if title and description and date_str and location and seats:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
                event = Event.objects.create(
                    title=title,
                    description=description,
                    date=date,
                    location=location,
                    seats=int(seats)
                )
                messages.success(request, f'Event "{title}" created successfully!')
                return redirect('manage_events')
            except ValueError:
                messages.error(request, 'Invalid date format.')
        else:
            messages.error(request, 'All fields are required.')
    
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'events/manage_events.html', {'events': events})


@login_required
@require_POST
def delete_event(request, event_id):
    # Check if user is admin
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    try:
        event = get_object_or_404(Event, id=event_id)
        event_title = event.title
        
        # Check if there are any bookings for this event
        from bookings.models import Booking
        booking_count = Booking.objects.filter(event=event).count()
        
        # Delete the event (this will cascade delete related bookings)
        event.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'Event "{event_title}" deleted successfully. {booking_count} related booking(s) were also deleted.'
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return JsonResponse({
            'success': False, 
            'message': f'Error deleting event: {str(e)}',
            'error_details': error_details
        })


@login_required
def edit_event(request, event_id):
    # Check if user is admin
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('event_list')
    
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        seats = request.POST.get('seats')
        
        if title and description and date_str and location and seats:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
                event.title = title
                event.description = description
                event.date = date
                event.location = location
                event.seats = int(seats)
                event.save()
                messages.success(request, f'Event "{title}" updated successfully!')
                return redirect('manage_events')
            except ValueError:
                messages.error(request, 'Invalid date format.')
        else:
            messages.error(request, 'All fields are required.')
    
    return render(request, 'events/edit_event.html', {'event': event})

