# Restrict the view to logged-in users only (redirects to login otherwise)
from django.contrib.auth.decorators import login_required
# 403 response for authenticated users who are NOT enrolled
from django.http import HttpResponseForbidden
from django.shortcuts import render
from courses.models import Course


@login_required
def course_chat_room(request, course_id):
    """Serves the chat room of a course for enrolled students only."""
    try:
        # SECURITY: fetch the course ONLY from the courses this user
        # is enrolled in (reverse many-to-many from Module 3)
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # Not enrolled (or course doesn't exist): deny access with 403
        return HttpResponseForbidden()
    # Render the chat room template with the course in the context
    return render(request, 'chat/room.html', {'course': course})
