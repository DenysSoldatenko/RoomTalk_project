from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from django.db.models import Count
from core.models import Room, Message, Topic, User
from .forms import UserRegistrationForm, RoomForm, UserForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid email or password.')

    return render(request, 'core/page_auth.html', {'page': 'login'})


def logout_user(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('home')
    elif request.method == 'POST':
        messages.error(request, 'An error occurred during registration. Please try again.')

    return render(request, 'core/page_auth.html', {'form': form, 'page': 'register'})


def home_view(request):
    q = request.GET.get('q', '')

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    ).select_related('host', 'topic').prefetch_related('participants').all()

    topics = Topic.objects.annotate(room_count=Count('room')).all()[:5]
    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[:3]

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'core/page_home.html', context)


def room_view(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    room_messages = room.message_set.select_related('user')
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room', room_slug=room.slug)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'core/page_room.html', context)


@login_required(login_url='login')
def create_or_update_room(request, room_slug=None):
    if room_slug:
        room = get_object_or_404(Room, slug=room_slug)
        if request.user != room.host:
            return HttpResponse('You are not allowed here!')

        form = RoomForm(request.POST or None, instance=room)
    else:
        room = None
        form = RoomForm(request.POST or None)

    topics = Topic.objects.all()

    if request.method == 'POST' and form.is_valid():
        topic_name = request.POST.get('topic_name')
        if topic_name:
            topic, created = Topic.objects.get_or_create(name=topic_name)

            if not room:  # Creating a new room
                Room.objects.create(
                    host=request.user,
                    topic=topic,
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description']
                )
            else:  # Updating the existing room
                room.topic = topic
                room.name = form.cleaned_data['name']
                room.description = form.cleaned_data['description']
                room.save()

            return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'core/page_room_create.html', context)


@login_required(login_url='login')
def delete_room(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'core/component_delete.html', {'obj': room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = get_object_or_404(Message, id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('room', room_slug=message.room.slug)

    return render(request, 'core/component_delete.html', {'obj': message})


@login_required(login_url='login')
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)

    rooms = user.room_set.all().select_related('topic').prefetch_related('participants')
    room_messages = user.message_set.select_related('room').all()

    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
    }

    return render(request, 'core/page_user_profile.html', context)


@login_required(login_url='login')
def update_user(request):
    form = UserForm(request.POST or None, request.FILES or None, instance=request.user)

    if form.is_valid():
        form.save()
        return redirect('user-profile', pk=request.user.id)

    return render(request, 'core/page_user_update.html', {'form': form})


def topics_page(request):
    q = request.GET.get('q', '')
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'core/page_topics.html', {'topics': topics})


def activity_page(request):
    room_messages = Message.objects.all()
    return render(request, 'core/page_activity.html', {'room_messages': room_messages})
