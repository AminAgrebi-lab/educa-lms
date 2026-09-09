# Aggregation for the annotated subjects queryset
from django.db.models import Count
# 404 helper for the custom enrollment view
from django.shortcuts import get_object_or_404
# HTTP Basic auth: credentials travel in the Authorization header
from rest_framework.authentication import BasicAuthentication
# Only logged-in users may enroll
from rest_framework.permissions import IsAuthenticated
# DRF's Response object and the base APIView class
from rest_framework.response import Response
from rest_framework.views import APIView
# ViewSets bundle list/retrieve actions in one class
from rest_framework import viewsets
from courses.api.pagination import StandardPagination
from courses.api.serializers import CourseSerializer, SubjectSerializer
from courses.models import Course, Subject


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only list() and retrieve() endpoints for courses."""
    # prefetch_related avoids one extra SQL query per serialized course
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only list() and retrieve() endpoints for subjects."""
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class CourseEnrollView(APIView):
    """POST-only endpoint: enrolls the authenticated user in a course."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        # 404 if the course ID in the URL does not exist
        course = get_object_or_404(Course, pk=pk)
        # Many-to-many: attach the requesting user to the course
        course.students.add(request.user)
        return Response({'enrolled': True})