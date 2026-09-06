# Mixins to restrict access: login required + specific permission required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
# get_object_or_404 fetches an object or raises 404; redirect sends to a URL
from django.shortcuts import get_object_or_404, redirect
# reverse_lazy resolves the URL lazily (when needed), not at import time
from django.urls import reverse_lazy
# TemplateResponseMixin renders templates; View is the base class-based view
from django.views.generic.base import TemplateResponseMixin, View
# Django's generic editing views for CRUD operations
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import ModuleFormSet
from .models import Course


class OwnerMixin:
    """Mixin: filters any QuerySet by the current user (owner)."""
    def get_queryset(self):
        qs = super().get_queryset()
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


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """Handles the formset to add, update, and delete course modules."""
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        # Build the formset for the current course, with optional POST data
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        # SECURITY: fetch the course ONLY if it belongs to the current user
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user
        )
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )