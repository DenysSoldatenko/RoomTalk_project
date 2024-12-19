from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_view, name="register"),

    path('', views.home_view, name="home"),

    path('room/<slug:room_slug>/', views.room_view, name="room"),
    path('create-room/', views.create_room, name="room-create"),
    path('update-room/<slug:room_slug>/', views.update_room, name="room-update"),
    path('delete-room/<slug:room_slug>/', views.delete_room, name="room-update"),

    path('delete-message/<str:pk>/', views.delete_message, name="message-delete"),

    path('profile/<str:pk>/', views.user_profile, name="user-profile"),
    path('update-user/', views.update_user, name="user-update"),

    # path('topics/', views.topicsPage, name="topics"),
    # path('activity/', views.activityPage, name="activity"),
]