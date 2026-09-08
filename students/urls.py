from django.urls import path
# Decorator that caches the full rendered output of a view, per URL
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    # Public signup page for new students
    path(
        'register/',
        views.StudentRegistrationView.as_view(),
        name='student_registration'
    ),
    # POST-only endpoint to enroll the current user in a course
    path(
        'enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'
    ),
    # List the courses the current student is enrolled in
    path(
        'courses/',
        views.StudentCourseListView.as_view(),
        name='student_course_list'
    ),
    # Student course page cached for 15 minutes per URL
    path(
        'course/<pk>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail'
    ),
    path(
        'course/<pk>/<module_id>/',
        cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module'
    ),
]