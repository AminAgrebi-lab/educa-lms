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
    # Edit an existing course
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
    # Manage the modules of a specific course (formset)
    path(
        '<pk>/module/',
        views.CourseModuleUpdateView.as_view(),
        name='course_module_update'
    ),
    # Create new content of a given type inside a module
    path(
        'module/<int:module_id>/content/<model_name>/create/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_create'
    ),
    # Update an existing content object of a given type
    path(
        'module/<int:module_id>/content/<model_name>/<id>/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_update'
    ),
    # Delete a content object (and its linked item)
    path(
        'content/<int:id>/delete/',
        views.ContentDeleteView.as_view(),
        name='module_content_delete'
    ),
    # List the contents of a specific module (with the modules sidebar)
    path(
        'module/<int:module_id>/',
        views.ModuleContentListView.as_view(),
        name='module_content_list'
    ),
]