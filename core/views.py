from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

from core.models import Room, Message, Topic
from .forms import UserRegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'core/page_auth.html', {'page': 'login'})

def logout_user(request):
    logout(request)
    return redirect('home')

def register_view(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration. Please try again.')

    return render(request, 'core/page_auth.html', {'form': form, 'page': 'register'})


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

    return render(request, 'core/page_home.html', context)

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
    return render(request, 'core/page_room.html', context)

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
