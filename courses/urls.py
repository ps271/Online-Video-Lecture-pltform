from django.urls import path, include
from django.contrib import admin
from . import views
from .views import CreateVideo, DetailVideo, UpdateVideo, DeleteVideo, VideoCategoryList
app_name = "courses"

urlpatterns = [
    path('', views.Index.as_view(), name = "home"),
    path('user-uploads/<str:username>', views.UserUploads.as_view(), name = "user-uploads"),
    path('create-video',  CreateVideo.as_view(), name='video-create'),
    path('<int:pk>/', DetailVideo.as_view(), name='video-detail'),
    path('<int:pk>/update-video', UpdateVideo.as_view(), name='video-update'),
    path('<int:pk>/delete-video', DeleteVideo.as_view(), name='video-delete'),
    path('category/<int:pk>', VideoCategoryList.as_view(), name='category-list'),
    path('search/', views.VideoSearch.as_view(), name='search-list'),
    path('like/', views.Like.as_view(), name='like'),
]