# apps.get_model() retrieves a model class dynamically by its name
from django.apps import apps
# Mixins to restrict access: login required + specific permission required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
# modelform_factory builds a ModelForm dynamically for any model
from django.forms.models import modelform_factory
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
from .models import Content, Course, Module
# Third-party mixins: skip CSRF check + parse/return JSON automatically
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

# Count() aggregation + annotate() to attach totals to each object in one query
from django.db.models import Count
from .models import Subject

# Generic view to display a single object by pk or slug
from django.views.generic.detail import DetailView

# Cross-app import: enrollment form built in the students app
from students.forms import CourseEnrollForm

# The low-level cache API (default cache backend)
from django.core.cache import cache


class CourseDetailView(DetailView):
    """Public view: displays the overview of a single course."""
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pre-fill the hidden course field with the course being viewed
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object}
        )
        # NEW: flag telling the template whether the user is already enrolled
        context['enrolled'] = (
            self.request.user.is_authenticated
            and self.object.students.filter(
                pk=self.request.user.pk
            ).exists()
        )
        return context
  

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


class ContentCreateUpdateView(TemplateResponseMixin, View):
    """A single view that creates/updates ANY of the 4 content models."""
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        # SECURITY: only allow the four valid content model names
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(
                app_label='courses', model_name=model_name
            )
        return None

    def get_form(self, model, *args, **kwargs):
        # Build the form dynamically; exclude the auto-managed fields
        Form = modelform_factory(
            model, exclude=['owner', 'order', 'created', 'updated']
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        # SECURITY: the module must belong to a course owned by the user
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, owner=request.user
            )
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # Creating: link the new object to the module via Content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )


class ContentDeleteView(View):
    def post(self, request, id):
        # SECURITY: the content's module's course must belong to the user
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module
        # Delete the actual Text/Video/Image/File object first
        content.item.delete()
        # Then delete the Content container object
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """Displays the sidebar of modules + the contents of the selected module."""
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        # SECURITY: the module's course must belong to the current user
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Receives the new module order as JSON and updates it in the DB."""
    def post(self, request):
        # request_json is a dict like: {"3": 0, "1": 1, "2": 2}
        for id, order in self.request_json.items():
            # SECURITY: only update modules of courses owned by the user
            Module.objects.filter(
                id=id, course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """Receives the new content order as JSON and updates it in the DB."""
    def post(self, request):
        for id, order in self.request_json.items():
            # SECURITY: only update contents of the user's own courses
            Content.objects.filter(
                id=id, module__course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class CourseListView(TemplateResponseMixin, View):
    """Public view: lists all courses, optionally filtered by subject."""
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        # Attach the total number of courses to each subject (single query)
        subjects = Subject.objects.annotate(
            total_courses=Count('courses')
        )
        # Attach the total number of modules to each course (single query)
        courses = Course.objects.annotate(
            total_modules=Count('modules')
        )
        if subject:
            # Filter by the subject given in the URL (404 if slug invalid)
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses
            }
        )
