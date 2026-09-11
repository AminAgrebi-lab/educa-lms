import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone


class Command(BaseCommand):
    help = 'Sends an e-mail reminder to users registered more ' \
           'than N days that are not enrolled into any courses yet'

    def add_arguments(self, parser):
        # --days named argument: minimum registration age for the reminder
        parser.add_argument('--days', dest='days', type=int)

    def handle(self, *args, **options):
        emails = []
        subject = 'Enroll in a course'
        # 🚨 BOOK ODDITY fixed: the reading prints timezone.now().today(),
        # but .today() is a classmethod returning LOCAL naive time and
        # silently ignoring timezone awareness; the book's own prose
        # mandates the timezone-aware now. We take its .date() for the
        # __date__ lookup below.
        cutoff_date = (
            timezone.now() - datetime.timedelta(days=options['days'] or 0)
        ).date()
        # Annotate every user with their enrollment count, keep the zeros
        users = User.objects.annotate(
            course_count=Count('courses_joined')
        ).filter(course_count=0, date_joined__date__lte=cutoff_date)
        for user in users:
            message = f"""Dear {user.first_name},
We noticed that you didn't enroll in any courses yet.
What are you waiting for?"""
            emails.append(
                (
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
            )
        # ONE SMTP connection for ALL emails (optimized bulk sending)
        send_mass_mail(emails)
        self.stdout.write(f'Sent {len(emails)} reminders')