from django.urls import include, path
# Routers build ViewSet URLs dynamically (list, detail, etc.)
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('subjects', views.SubjectViewSet)

urlpatterns = [
    # Custom enrollment endpoint (POST only)
    path(
        'courses/<pk>/enroll/',
        views.CourseEnrollView.as_view(),
        name='course_enroll'
    ),
    # All router-generated ViewSet URLs
    path('', include(router.urls)),
]