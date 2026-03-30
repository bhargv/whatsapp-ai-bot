from django.urls import path
from . import views

urlpatterns = [
    path('process-message/', views.process_message, name='process_message'),
    path('status/', views.whatsapp_status, name='whatsapp_status'),
    path('history/<str:phone_number>/', views.conversation_history, name='conversation_history'),
    path('conversations/', views.list_conversations, name='list_conversations'),
    path('save-api-key/', views.save_api_key, name='save_api_key'),
    path('check-config/', views.check_config, name='check_config'),
    path('contacts/', views.get_contacts, name='get_contacts'),
    path('chats/', views.get_chats, name='get_chats'),
    path('reset-whatsapp/', views.reset_whatsapp, name='reset_whatsapp'),
]
