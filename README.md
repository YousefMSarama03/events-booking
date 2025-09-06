# Events Management System - Admin Dashboard

## Overview
This is a comprehensive admin dashboard for managing events, users, and bookings in the Events Management System. The dashboard provides administrators with powerful tools to monitor system activity and manage all aspects of the platform.

## Features

### 🎯 Admin Dashboard
- **Real-time Statistics**: View total users, events, and bookings at a glance
- **User Overview**: Breakdown of users by role (students, organizers, admins)
- **Event Analytics**: Track upcoming, past, and weekly events
- **Booking Insights**: Monitor confirmed vs cancelled bookings
- **Monthly Trends**: Visual representation of booking patterns over time
- **Recent Activities**: Live feed of latest bookings, events, and user registrations
- **Popular Events**: See which events are most popular based on bookings

### 👥 User Management
- **View All Users**: Complete list of registered users with detailed information
- **Role-based Filtering**: Filter users by role (student, organizer, admin)
- **Search Functionality**: Find users quickly by username
- **User Statistics**: See booking count and event participation for each user
- **User Actions**: Edit user details and manage roles (coming soon)

### 📅 Event Management
- **Create Events**: Add new events with title, description, date, location, and seats
- **Edit Events**: Modify existing event details
- **Delete Events**: Remove events with confirmation modal
- **Event Overview**: Comprehensive view of all events in the system

### 🔐 Security Features
- **Role-based Access Control**: Only users with 'admin' role can access dashboard
- **Authentication Required**: All admin functions require user login
- **CSRF Protection**: Secure form submissions with Django CSRF tokens

## Access Requirements

To access the admin dashboard, users must:
1. Be registered and logged into the system
2. Have the role set to 'admin' in their user profile
3. Navigate to `/accounts/admin-dashboard/`

## Navigation

### Main Navigation
- **Admin Dashboard**: Main overview page with statistics
- **Manage Events**: Create, edit, and delete events
- **Manage Users**: View and manage all system users

### Quick Access
- **Profile Page**: Admin users see an "Admin Dashboard" button
- **Navigation Bar**: Admin users see an "Admin Dashboard" link in the main navigation

## URLs

- **Admin Dashboard**: `/accounts/admin-dashboard/`
- **Manage Events**: `/events/manage-events/`
- **Edit Event**: `/events/edit-event/<id>/`
- **Manage Users**: `/accounts/manage-users/`

## Technical Implementation

### Backend
- **Django Views**: Role-based access control and data aggregation
- **Database Queries**: Optimized queries for statistics and user data
- **Security**: Login required decorators and role validation

### Frontend
- **Responsive Design**: Mobile-friendly interface with CSS Grid
- **Interactive Elements**: JavaScript for modals, filtering, and search
- **Real-time Updates**: Dynamic content loading and user feedback
- **Modern UI**: Clean, professional design with hover effects and animations

### Data Models
- **User**: Custom user model with role-based permissions
- **Event**: Event management with title, description, date, location, and seats
- **Booking**: Booking system linking users to events

## Usage Examples

### Creating a New Event
1. Navigate to "Manage Events" from the admin dashboard
2. Fill out the event creation form
3. Submit to create the event
4. Event appears in the events list

### Managing Users
1. Go to "Manage Users" from the admin dashboard
2. Use filters to find specific users
3. View user statistics and details
4. Edit user information or roles as needed

### Monitoring System Health
1. Check the main dashboard for key metrics
2. Review recent activities for any issues
3. Monitor booking trends and popular events
4. Track user growth and engagement

## Future Enhancements

- **Advanced Analytics**: More detailed reporting and charts
- **Bulk Operations**: Mass user/event management
- **Export Functionality**: Download reports and data
- **Notification System**: Alerts for system events
- **Audit Logs**: Track all admin actions
- **API Integration**: Connect with external systems

## Support

For technical support or feature requests, please contact the development team.

---

**Note**: This admin dashboard is designed for internal use by system administrators. Ensure proper security measures are in place when deploying to production environments.
