from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from bookings.models import Booking
from django.contrib.auth import get_user_model
from events.models import Event
from django.db.models import Count
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST

User = get_user_model()


@login_required
def show_profile(request):
    user = request.user
    bookings = Booking.objects.filter(student=request.user).count()
    return render(request,'accounts/profile.html', {'user':user,'bookings':bookings})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next') or 'event_list'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', { 'next': request.GET.get('next', '') })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def admin_dashboard(request):
    # Check if user is admin
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('profile')
    
    # Get current date and calculate date ranges
    now = datetime.now()
    today = now.date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # User statistics
    total_users = User.objects.count()
    students = User.objects.filter(role='student').count()
    organizers = User.objects.filter(role='organizer').count()
    admins = User.objects.filter(role='admin').count()
    new_users_week = User.objects.filter(date_joined__gte=last_week).count()
    new_users_month = User.objects.filter(date_joined__gte=last_month).count()
    
    # Event statistics
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=now).count()
    past_events = Event.objects.filter(date__lt=now).count()
    events_this_week = Event.objects.filter(date__gte=last_week, date__lte=today + timedelta(days=7)).count()
    
    # Booking statistics
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    bookings_this_week = Booking.objects.filter(booked_at__gte=last_week).count()
    bookings_this_month = Booking.objects.filter(booked_at__gte=last_month).count()
    
    # Recent activities
    recent_bookings = Booking.objects.select_related('student','event').order_by('-booked_at')[:10]
    recent_events = Event.objects.order_by('-created_at')[:10]
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Popular events (by number of bookings)
    popular_events = Event.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-booking_count')[:5]
    
    # Monthly booking trends (last 6 months)
    monthly_bookings = []
    max_count = 0
    
    # First pass: get all counts and find maximum
    for i in range(6):
        month_start = (now - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        count = Booking.objects.filter(booked_at__gte=month_start, booked_at__lte=month_end).count()
        max_count = max(max_count, count)
        monthly_bookings.append({
            'month': month_start.strftime('%B %Y'),
            'count': count
        })
    
    # Second pass: calculate relative heights (max 150px)
    chart_height = 150
    for month_data in monthly_bookings:
        if max_count > 0:
            month_data['height'] = int((month_data['count'] / max_count) * chart_height)
        else:
            month_data['height'] = 0
    
    monthly_bookings.reverse()
    
    context = {
        'total_users': total_users,
        'students': students,
        'organizers': organizers,
        'admins': admins,
        'new_users_week': new_users_week,
        'new_users_month': new_users_month,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events_this_week': events_this_week,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'bookings_this_week': bookings_this_week,
        'bookings_this_month': bookings_this_month,
        'recent_bookings': recent_bookings,
        'recent_events': recent_events,
        'recent_users': recent_users,
        'popular_events': popular_events,
        'monthly_bookings': monthly_bookings,
        'today': today,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def manage_users(request):
    # Check if user is admin
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('profile')
    
    # Get all users with their statistics
    users = User.objects.all().order_by('-date_joined')
    
    # Add additional context for each user
    for user in users:
        user.booking_count = Booking.objects.filter(student=user).count()
        user.event_count = Event.objects.filter(created_at__gte=user.date_joined).count()
    
    context = {
        'users': users,
    }
    
    return render(request, 'accounts/manage_users.html', context)


@login_required
def edit_user(request, user_id):
    # Check if user is admin
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        if request.method == 'POST':
            # Get form data
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            role = request.POST.get('role')
            
            # Validate required fields
            if not username or not email or not role:
                return JsonResponse({'success': False, 'message': 'Username, email, and role are required'})
            
            # Check if username is already taken by another user
            if User.objects.exclude(id=user_id).filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username is already taken'})
            
            # Check if email is already taken by another user
            if User.objects.exclude(id=user_id).filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email is already taken'})
            
            # Update user
            user.username = username
            user.first_name = first_name or ''
            user.last_name = last_name or ''
            user.email = email
            user.role = role
            user.save()
            
            return JsonResponse({
                'success': True, 
                'message': f'User "{username}" updated successfully'
            })
        
        # GET request - return user data
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role
            }
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return JsonResponse({
            'success': False, 
            'message': f'Error updating user: {str(e)}',
            'error_details': error_details
        })


@login_required
@require_POST
def delete_user(request, user_id):
    # Check if user is admin
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Prevent admin from deleting themselves
        if user.id == request.user.id:
            return JsonResponse({'success': False, 'message': 'You cannot delete your own account'})
        
        # Prevent deletion of other admins
        if user.role == 'admin':
            return JsonResponse({'success': False, 'message': 'Cannot delete admin users'})
        
        username = user.username
        
        # Delete the user (this will cascade delete related bookings)
        user.delete()
        
        return JsonResponse({
            'success': True, 
            'message': f'User "{username}" deleted successfully'
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return JsonResponse({
            'success': False, 
            'message': f'Error deleting user: {str(e)}',
            'error_details': error_details
        })