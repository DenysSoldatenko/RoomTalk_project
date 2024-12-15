import os
import random
from io import BytesIO

import requests
from PIL import Image
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker

from core.models import User, Topic, Room, Message


class Command(BaseCommand):
    help = "Generate fake data for User, Topic, Room, and Message models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create fake Topics
        topics = []
        for _ in range(5):
            topic_name = fake.word().capitalize()

            try:
                topic = Topic.objects.create(name=topic_name)
                topics.append(topic)
                self.stdout.write(self.style.SUCCESS(f'Successfully created topic: {topic.name}'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'Topic name "{topic_name}" already exists. Skipping this topic.'))
                continue

        # Create fake Users (custom user model)
        users = []
        for _ in range(10):
            name = fake.name()
            email = fake.unique.email()
            username = fake.user_name()
            bio = fake.text()
            avatar_url = fake.image_url()

            # Fetch image
            try:
                response = requests.get(avatar_url)
                if response.status_code == 200:
                    image_name = os.path.basename(avatar_url)
                    if not image_name.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp')):
                        image_name += '.jpg'

                    image = Image.open(BytesIO(response.content))

                    if image.mode != 'RGB':
                        image = image.convert('RGB')

                    image = image.resize((300, 300))

                    image_io = BytesIO()
                    image.save(image_io, format='JPEG')
                    image_io.seek(0)

                    avatar_content = ContentFile(image_io.read(), name=image_name)

                    user = User.objects.create(
                        username=username,
                        email=email,
                        name=name,
                        bio=bio,
                        avatar=avatar_content
                    )
                    users.append(user)
                    self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))

            except requests.RequestException as e:
                self.stdout.write(self.style.WARNING(f'Failed to download avatar for user "{username}". Error: {e}'))
                continue

        # Create fake Rooms
        rooms = []
        for _ in range(15):
            room_name = fake.word().capitalize()

            # Check if room name already exists
            while Room.objects.filter(name=room_name).exists():
                room_name = fake.word().capitalize()  # Generate a new name if the name already exists

            room_description = fake.text()
            room_host = random.choice(users)  # Randomly assign a user as host
            room_topic = random.choice(topics)  # Randomly assign a topic

            room = Room.objects.create(
                name=room_name,
                description=room_description,
                host=room_host,
                topic=room_topic
            )

            # Add random users to the room as participants
            for user in random.sample(users, random.randint(1, 5)):  # Pick 1 to 5 random users
                room.participants.add(user)

            rooms.append(room)
            self.stdout.write(self.style.SUCCESS(f'Successfully created room: {room.name}'))

        # Create fake Messages
        for _ in range(50):
            message_body = fake.text()
            room = random.choice(rooms)  # Randomly pick a room
            user = random.choice(users)  # Randomly pick a user

            Message.objects.create(
                user=user,
                room=room,
                body=message_body
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created message in room: {room.name}'))
