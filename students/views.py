# Built-in helpers to verify credentials and start an authenticated session
from django.contrib.auth import authenticate, login
# Restrict views to logged-in users only
from django.contrib.auth.mixins import LoginRequiredMixin
# Ready-made ModelForm that creates a User with password validation
from django.contrib.auth.forms import UserCreationForm
# reverse_lazy resolves URLs lazily (when needed), not at import time
from django.urls import reverse_lazy
# Generic views: creation, form handling, listing, and detail views
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# The Course model lives in the courses app (cross-app import)
from courses.models import Course
from .forms import CourseEnrollForm
from django.shortcuts import redirect



class StudentRegistrationView(CreateView):
    """Public view: creates a new student account and logs them in."""
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        # Save the new user first
        result = super().form_valid(form)
        cd = form.cleaned_data
        # Verify the credentials of the user we just created
        user = authenticate(
            username=cd['username'], password=cd['password1']
        )
        # Start an authenticated session immediately (no second login)
        login(self.request, user)
        return result



class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'student_course_detail', args=[self.course.id]
        )

    # ✅ إضافة جديدة لمنع الانهيار وطباعة سبب الخطأ
    def form_invalid(self, form):
        # Print the exact validation error to your terminal (PowerShell)
        print(f"🚨 ENROLLMENT FORM ERRORS: {form.errors}")
        # Redirect to the main catalog instead of crashing with a 500 error
        return redirect('course_list')


class StudentCourseListView(LoginRequiredMixin, ListView):
    """Lists only the courses the current student is enrolled in."""
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # Filter via the many-to-many field: courses containing this student
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    """Displays one enrolled course with its modules and contents."""
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # SECURITY: students can only open courses they are enrolled in
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # Show the specific module given in the URL
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # Default: show the first module of the course
            context['module'] = course.modules.all()[0]
        return context