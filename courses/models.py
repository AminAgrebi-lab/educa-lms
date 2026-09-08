from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Import the custom OrderField from the fields.py file we created
from .fields import OrderField


class Subject(models.Model):
    """Represents a broad subject area (e.g., Mathematics, Programming)."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']  # Sort subjects alphabetically

    def __str__(self):
        return self.title


class Course(models.Model):
    """Represents a specific course within a subject."""
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    # Many-to-many: the students enrolled in this course (Module 3)
    # THIS FIELD WAS MISSING!
    students = models.ManyToManyField(
        User,
        related_name='courses_joined',  # Reverse lookup: user.courses_joined.all()
        blank=True                      # A course can exist with zero students
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    """Represents a module/section within a specific course."""
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Auto-calculate order relative to the course this module belongs to
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        # Display the module with its order, e.g., "0. Module 1"
        return f'{self.order}. {self.title}'


class ItemBase(models.Model):
    """Abstract base model shared by all content types (no DB table)."""
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    """Stores text content."""
    content = models.TextField()


class File(ItemBase):
    """Stores uploaded files (e.g., PDFs) in media/files/."""
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """Stores uploaded images in media/images/."""
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """Stores an embeddable video URL."""
    url = models.URLField()


class Content(models.Model):
    """Generic container linking a module to any content type."""
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    # Restrict the generic relation to ONLY our four content models
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('text', 'video', 'image', 'file')
        }
    )
    object_id = models.PositiveIntegerField()
    # Virtual field combining content_type + object_id
    item = GenericForeignKey('content_type', 'object_id')
    # Auto-calculate order relative to the module this content belongs to
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']