from django.urls import path
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
    # Detail page of an enrolled course (first module by default)
    path(
        'course/<pk>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail'
    ),
    # Detail page of an enrolled course for a specific module
    path(
        'course/<pk>/<module_id>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail_module'
    ),
]