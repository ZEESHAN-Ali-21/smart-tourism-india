from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatSession(models.Model):
    """Chat session for tracking user conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # User context for better responses
    user_location = models.CharField(max_length=100, blank=True)
    user_preferences = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"Session {self.session_id} - {self.user.username if self.user else 'Anonymous'}"
    
    def get_message_count(self):
        return self.messages.count()


class ChatMessage(models.Model):
    """Individual chat messages"""
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('bot', 'Bot Response'),
        ('system', 'System Message'),
    ]
    
    INPUT_TYPES = [
        ('text', 'Text Input'),
        ('voice', 'Voice Input'),
        ('quick_reply', 'Quick Reply'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    input_type = models.CharField(max_length=20, choices=INPUT_TYPES, default='text')
    
    # Message content
    message = models.TextField()
    original_voice_text = models.TextField(blank=True, help_text="Original voice-to-text content")
    
    # AI Response metadata
    confidence_score = models.FloatField(null=True, blank=True)
    intent_detected = models.CharField(max_length=100, blank=True)
    entities_extracted = models.JSONField(default=dict, blank=True)
    
    # Response context
    destinations_mentioned = models.JSONField(default=list, blank=True)
    categories_mentioned = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.IntegerField(null=True, blank=True, help_text="Response time in milliseconds")
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.get_message_type_display()}: {self.message[:50]}..."


class ChatFeedback(models.Model):
    """User feedback on bot responses"""
    FEEDBACK_TYPES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('incorrect', 'Incorrect Information'),
        ('irrelevant', 'Irrelevant Response'),
    ]
    
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['message', 'user']
    
    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.message.message[:30]}..."


class ChatAnalytics(models.Model):
    """Analytics for chatbot performance"""
    date = models.DateField(auto_now_add=True)
    total_sessions = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    unique_users = models.IntegerField(default=0)
    
    # Popular topics
    popular_intents = models.JSONField(default=dict)
    popular_destinations = models.JSONField(default=dict)
    popular_categories = models.JSONField(default=dict)
    
    # Performance metrics
    average_response_time = models.FloatField(default=0.0)
    user_satisfaction_score = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ['date']
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"
