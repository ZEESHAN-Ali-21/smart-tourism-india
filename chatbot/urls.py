from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Main chat interface
    path('', views.ChatView.as_view(), name='chat'),
    
    # AJAX endpoints
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/voice-to-text/', views.voice_to_text, name='voice_to_text'),
    path('api/chat-history/', views.get_chat_history, name='chat_history'),
    path('api/feedback/', views.submit_feedback, name='submit_feedback'),
]