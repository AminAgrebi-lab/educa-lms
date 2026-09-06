# Mixins to restrict access: login required + specific permission required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
# reverse_lazy resolves the URL lazily (when needed), not at import time
from django.urls import reverse_lazy
# Django's generic editing views for CRUD operations
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import Course


class OwnerMixin:
    """Mixin: filters any QuerySet by the current user (owner)."""
    def get_queryset(self):
        qs = super().get_queryset()
        # Object-level security: users only access their own objects
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    """Mixin: automatically assigns the current user as owner on save."""
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(
    OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin
):
    """Common configuration + access restriction for course views."""
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'