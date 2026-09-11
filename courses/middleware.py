from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Course


def subdomain_course_middleware(get_response):
    """
    Subdomains for courses:
    <course-slug>.educaproject.com  →  educaproject.com/course/<slug>/
    """
    def middleware(request):
        # 🚨 BOOK TYPO fixed: the reading prints split('.').  (stray dot = SyntaxError)
        host_parts = request.get_host().split('.')
        # Subdomain present? (more than domain+TLD) and not 'www'
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # 404 if no course matches the subdomain slug
            course = get_object_or_404(Course, slug=host_parts[0])
            course_url = reverse('course_detail', args=[course.slug])
            # Rebuild the URL on the parent domain, keeping scheme and port
            url = '{}://{}{}'.format(
                request.scheme, '.'.join(host_parts[1:]), course_url
            )
            # Short-circuit: redirect WITHOUT calling get_response
            return redirect(url)
        response = get_response(request)
        return response
    return middleware