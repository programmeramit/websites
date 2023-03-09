from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.rooms,name="room"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>',views.updateRoom,name="updateRoom"),
    path('delete-room/<str:pk>',views.deleteRoom,name="deleteRoom"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('Userprofile/<str:pk>',views.Userprofile,name="user-profile"),
    path('topics',views.topics,name="topics"),
    path('activity',views.topics,name="activity")



]
