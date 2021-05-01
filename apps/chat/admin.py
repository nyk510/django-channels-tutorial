from django.contrib import admin

from . import models


# Register your models here.

@admin.register(models.ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'title', 'created_at',)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'text', 'author',)
