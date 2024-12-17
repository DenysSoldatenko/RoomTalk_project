from django.shortcuts import redirect, get_object_or_404, render
from core.models import Room, Message, Topic

def home_view(request):
    topics = Topic.objects.all()[:5]
    rooms = Room.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.all()[:3]

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages
    }

    return render(request, 'core/home_page.html', context)

def room_view(request, room_slug):
    room = get_object_or_404(Room.objects.select_related('topic'), slug=room_slug)
    room_messages = room.message_set.select_related('user').all()
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', room_slug=room.slug)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'core/room_page.html', context)

def create_room(request):
    return None

def update_room(request):
    return None

def delete_room(request):
    return None

def delete_message(request):
    return None

def user_profile(request):
    return None

def update_user(request):
    return None
