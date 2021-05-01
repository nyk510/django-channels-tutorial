from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    room_id = models.CharField(help_text='チャットに固有のid', max_length=32, unique=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return f'{self.room_id} {self.title}'


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True, null=True)