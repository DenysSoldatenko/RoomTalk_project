from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.loginPage, name="login"),
    # path('logout/', views.logoutUser, name="logout"),
    # path('register/', views.registerPage, name="register"),

    path('', views.home_view, name="home"),

    path('room/<slug:room_slug>/', views.room_view, name="room"),
    path('create-room/', views.create_room, name="create-room"),
    path('update-room/<slug:room_slug>/', views.update_room, name="update-room"),
    path('delete-room/<slug:room_slug>/', views.delete_room, name="delete-room"),

    path('delete-message/<str:pk>/', views.delete_message, name="delete-message"),

    path('profile/<str:pk>/', views.user_profile, name="profile-user"),
    path('update-user/', views.update_user, name="update-user"),

    # path('topics/', views.topicsPage, name="topics"),
    # path('activity/', views.activityPage, name="activity"),
]