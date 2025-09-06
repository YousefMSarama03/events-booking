import time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


class InactiveUserLogoutMiddleware:
	"""Logs out authenticated users after SESSION_IDLE_TIMEOUT seconds of inactivity.

	Stores the last activity as an epoch seconds integer in the session under
	'last_activity'. On each authenticated request, if the elapsed time exceeds
	the configured timeout, the user is logged out and redirected to LOGIN_URL.
	"""

	def __init__(self, get_response):
		self.get_response = get_response
		self.timeout_seconds = int(getattr(settings, 'SESSION_IDLE_TIMEOUT', 300))

	def __call__(self, request):
		# Bypass for unauthenticated users
		if request.user.is_authenticated:
			now = int(time.time())
			last_activity = request.session.get('last_activity')

			# Determine if current path should skip redirect to avoid loops
			login_path = reverse(getattr(settings, 'LOGIN_URL', 'login'))
			is_auth_path = request.path.startswith(login_path)

			if last_activity is not None and now - int(last_activity) > self.timeout_seconds:
				logout(request)
				# Flush session to clear stale data
				request.session.flush()
				if not is_auth_path:
					messages.info(request, 'You were logged out due to inactivity.')
					return redirect(login_path)

			# Update last activity timestamp for rolling timeout
			request.session['last_activity'] = now

		response = self.get_response(request)
		return response

