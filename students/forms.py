from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    # Hidden field carrying the ID of the course to enroll in
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),  # Empty queryset: no DB hit at import time
        widget=forms.HiddenInput         # Rendered as a hidden input, not a select
    )

    def __init__(self, *args, **kwargs):
        # CORRECT signature (the reading text has a typo: `def __init__(self, form):`)
        super().__init__(*args, **kwargs)
        # Populate the real queryset only when the form is instantiated
        self.fields['course'].queryset = Course.objects.all()