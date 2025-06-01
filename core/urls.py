from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('video/<int:video_id>/', views.video_detail_view, name='video_detail'),
    path('search/', views.search_view, name='search'),
    path('video/upload/', views.video_upload_view, name='video_upload'),
    path('topic/<int:topic_id>/toggle/', views.toggle_topic_completion, name='toggle_topic'),
    path('topic/add-video/', views.add_video_to_topic, name='add_video_to_topic'),
    path('progress/', views.progress_view, name='progress'),
] 