# videostreamingapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('api/videos/', views.create_video, name='create_video'),
    path('api/videos/<int:pk>/', views.video_detail, name='video_detail'),
    path('api/videos/search/', views.search_videos, name='search_videos'),
    path('api/videos/list/', views.list_videos, name='list_videos'),
]
