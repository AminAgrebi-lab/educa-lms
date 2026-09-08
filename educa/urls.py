from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
# include() allows attaching the URLconf of the courses app
from django.urls import include, path
# Import the public course list view for the root URL
from courses.views import CourseListView

urlpatterns = [
    # Public course catalog at the ROOT URL
    path('', CourseListView.as_view(), name='course_list'),
    # Login page URL using Django's built-in LoginView
    path(
        'accounts/login/', auth_views.LoginView.as_view(), name='login'
    ),
    # Logout URL using Django's built-in LogoutView (accepts POST only)
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    # Django administration site
    path('admin/', admin.site.urls),
    # Include the courses app URL patterns under the 'course/' prefix
    path('course/', include('courses.urls')),
        # Include the students app URL patterns under the 'students/' prefix
    path('students/', include('students.urls')),
]

# Serve media files during development only (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )