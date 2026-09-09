# DRF's serializer classes for converting model instances to/from JSON
from rest_framework import serializers
from courses.models import Course, Module, Subject


class SubjectSerializer(serializers.ModelSerializer):
    """Serializes Subject instances into JSON-ready Python data."""
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class ModuleSerializer(serializers.ModelSerializer):
    """Nested representation of a module inside a course."""
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """Serializes a course with its modules fully nested."""
    # Nest full module objects instead of raw primary keys
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'subject', 'title', 'slug',
            'overview', 'created', 'owner', 'modules',
        ]