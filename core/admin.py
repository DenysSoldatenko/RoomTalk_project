from django.contrib import admin
from .models import ProjectUser, Topic, Room, Message

@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'name', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'topic', 'created', 'updated')
    search_fields = ('name', 'host__email', 'topic__name')
    list_filter = ('host', 'topic')
    ordering = ('-created',)
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'body', 'created', 'updated')
    search_fields = ('body', 'user__email', 'room__name')
    list_filter = ('room', 'user')
    ordering = ('-created',)
