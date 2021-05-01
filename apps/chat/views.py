from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import ChatRoom


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    room = get_object_or_404(ChatRoom, room_id=room_name)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'room': room,
        'messages': room.messages.all()
    })
