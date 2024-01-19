from django.db import models
from django.utils import timezone

class Chat(models.Model):
    chat_id = models.IntegerField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    authorization_flag = models.BooleanField(default=False)
    puzzle_requested = models.IntegerField(default=0)
    solution_count = models.IntegerField(default=0)
    last_access = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Chat {self.chat_id} ({self.phone_number})"


class AuthorizedPhoneNumber(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone_number
    
class Indizi(models.Model):
    path = models.TextField()
    solution = models.TextField()

    def __str__(self):
        return f"Indizi {self.id}"
    
class UserMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from Chat {self.chat.chat_id} at {self.timestamp}"