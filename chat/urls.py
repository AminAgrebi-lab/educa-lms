from django.urls import path
from . import views

# Namespace for reversing chat URLs as 'chat:<name>'
app_name = 'chat'

urlpatterns = [
    # Chat room of a given course; course_id must be an integer
    path(
        'room/<int:course_id>/',
        views.course_chat_room,
        name='course_chat_room'
    ),
]