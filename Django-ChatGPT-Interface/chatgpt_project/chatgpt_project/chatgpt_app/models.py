from django.db import models

class Conversation(models.Model):
    user_input = models.CharField(max_length=200)
    bot_response = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
