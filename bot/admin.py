from django.contrib import admin
from .models import Message, Conversation

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'message_text', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['phone_number', 'message_text']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'last_interaction']
    search_fields = ['phone_number']
