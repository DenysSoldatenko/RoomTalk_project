from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_view, name="register"),

    path('', views.home_view, name="home"),

    path('room/<slug:room_slug>/', views.room_view, name="room"),
    path('room-create/', views.create_or_update_room, name="room-create"),
    path('room-update/<slug:room_slug>/', views.create_or_update_room, name="room-update"),
    path('room-delete/<slug:room_slug>/', views.delete_room, name="room-delete"),

    path('message-delete/<str:pk>/', views.delete_message, name="message-delete"),

    path('user-profile/<str:pk>/', views.user_profile, name="user-profile"),
    path('user-update/', views.update_user, name="user-update"),

    path('topics/', views.topics_page, name="topics"),
    path('activity/', views.activity_page, name="activity"),
]