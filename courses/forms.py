# inlineformset_factory builds a formset for objects related to a parent object
from django.forms.models import inlineformset_factory
from .models import Course, Module

# Build a formset to manage the Module objects related to a Course object
ModuleFormSet = inlineformset_factory(
    Course,          # The parent model
    Module,          # The related (child) model
    fields=['title', 'description'],  # Fields included in each form
    extra=2,         # Display 2 empty extra forms for adding new modules
    can_delete=True  # Add a delete checkbox to each existing module form
)