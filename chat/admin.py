from django.contrib import admin
from chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sent_on', 'user', 'course', 'content']
    list_filter = ['sent_on', 'course']
    search_fields = ['content']
    # 🚨 BOOK TYPO: the reading writes ['user', 'content'] but 'content' is a
    # TextField! raw_id_fields only accepts foreign keys → the correct
    # fields are the two FKs: user and course
    raw_id_fields = ['user', 'course']
