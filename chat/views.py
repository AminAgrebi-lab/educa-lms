# Restrict the view to logged-in users only (redirects to login otherwise)
from django.contrib.auth.decorators import login_required
# 403 response for authenticated users who are NOT enrolled
from django.http import HttpResponseForbidden
from django.shortcuts import render
from courses.models import Course


@login_required
def course_chat_room(request, course_id):
    try:
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponseForbidden()
    # Last 5 messages, newest first, with user fetched in the same query
    latest_messages = course.chat_messages.select_related(
        'user'
    ).order_by('-id')[:5]
    # Flip back to chronological order for display
    latest_messages = reversed(latest_messages)
    return render(
        request,
        'chat/room.html',
        {'course': course, 'latest_messages': latest_messages}
    )
