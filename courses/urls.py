from django.urls import path
from . import views

urlpatterns = [
    # List the courses created by the current user
    path(
        'mine/',
        views.ManageCourseListView.as_view(),
        name='manage_course_list'
    ),
    # Create a new course
    path(
        'create/',
        views.CourseCreateView.as_view(),
        name='course_create'
    ),
    # Edit an existing course (pk = primary key of the course)
    path(
        '<pk>/edit/',
        views.CourseUpdateView.as_view(),
        name='course_edit'
    ),
    # Delete a course
    path(
        '<pk>/delete/',
        views.CourseDeleteView.as_view(),
        name='course_delete'
    ),
]