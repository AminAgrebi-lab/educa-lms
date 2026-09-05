from django.contrib import admin
from .models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug'] # Columns to display in the admin list view
    prepopulated_fields = {'slug': ('title',)} # Automatically fills the slug field based on the title


# Define Module as an inline model to be edited directly inside the Course admin page
class ModuleInline(admin.StackedInline):
    model = Module
    extra = 0 # Do not show extra empty forms by default


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject'] # Add sidebar filters for easy searching
    search_fields = ['title', 'overview'] # Add a search bar for these specific fields
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline] # Attach the ModuleInline to manage modules from the course page
