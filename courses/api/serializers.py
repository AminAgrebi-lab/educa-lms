# DRF's serializer classes for converting model instances to/from JSON
from rest_framework import serializers
from courses.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    """Serializes Subject instances into JSON-ready Python data."""
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']