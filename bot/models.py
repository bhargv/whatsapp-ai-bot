from django.db import models

class Message(models.Model):
    phone_number = models.CharField(max_length=50)
    message_text = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.phone_number} - {self.timestamp}"

class Conversation(models.Model):
    phone_number = models.CharField(max_length=50, unique=True)
    context = models.JSONField(default=list)
    last_interaction = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation with {self.phone_number}"
