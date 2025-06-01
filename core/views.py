from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Avg, Sum
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import User, Subject, Video, Topic, TopicProgress

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST.get('phone_number')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            phone_number=phone_number
        )
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('dashboard')

    return render(request, 'core/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def dashboard_view(request):
    subjects = Subject.objects.filter(created_by=request.user)
    
    # Calculate progress for each subject
    for subject in subjects:
        total_videos = subject.videos.count()
        watched_videos = subject.videos.filter(views__gt=0).count()
        subject.progress = (watched_videos / total_videos * 100) if total_videos > 0 else 0
    
    # Get recent videos
    recent_videos = Video.objects.filter(subject__created_by=request.user).order_by('-upload_date')[:5]
    
    # Calculate overall statistics
    total_videos = Video.objects.filter(subject__created_by=request.user).count()
    watched_videos = Video.objects.filter(subject__created_by=request.user, views__gt=0).count()
    completion_rate = (watched_videos / total_videos * 100) if total_videos > 0 else 0
    
    # Calculate total hours watched
    total_seconds = Video.objects.filter(
        subject__created_by=request.user,
        views__gt=0,
        duration__isnull=False
    ).aggregate(total_duration=Sum('duration'))['total_duration'] or 0
    hours_watched = round(total_seconds / 3600, 1)  # Convert seconds to hours

    context = {
        'subjects': subjects,
        'recent_videos': recent_videos,
        'total_videos': total_videos,
        'hours_watched': hours_watched,
        'completion_rate': round(completion_rate, 1)
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def progress_view(request):
    subjects = Subject.objects.filter(created_by=request.user).annotate(
        total_videos=Count('videos'),
        watched_videos=Count('videos', filter=Q(videos__views__gt=0))
    )

    total_videos = sum(subject.total_videos for subject in subjects)
    videos_watched = sum(subject.watched_videos for subject in subjects)
    overall_progress = (videos_watched / total_videos * 100) if total_videos > 0 else 0

    for subject in subjects:
        subject.progress = (subject.watched_videos / subject.total_videos * 100) if subject.total_videos > 0 else 0
        subject.last_studied = subject.videos.filter(views__gt=0).order_by('-updated_at').first()

    study_hours = sum(video.duration for video in Video.objects.filter(
        subject__created_by=request.user,
        views__gt=0,
        duration__isnull=False
    )) / 3600  # Convert seconds to hours

    context = {
        'subjects': subjects,
        'total_subjects': subjects.count(),
        'videos_watched': videos_watched,
        'study_hours': round(study_hours, 1),
        'overall_progress': round(overall_progress, 1),
    }
    return render(request, 'core/progress.html', context)

@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    topics = subject.topics.all().prefetch_related('progress')
    videos = Video.objects.filter(subject=subject)
    
    total_topics = topics.count()
    completed_topics = sum(1 for topic in topics if topic.progress.filter(user=request.user, is_completed=True).exists())
    progress_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0
    
    context = {
        'videos': videos,
        'topics': topics,
        'completed_topics': completed_topics,
        'total_topics': total_topics,
        'progress_percentage': round(progress_percentage, 1)
    }
    return render(request, 'core/subject_detail.html', context)

@login_required
def video_detail_view(request, video_id):
    video = get_object_or_404(Video, id=video_id, subject__created_by=request.user)
    
    # Increment view count
    if not request.session.get(f'video_{video_id}_viewed', False):
        video.views += 1
        video.save()
        request.session[f'video_{video_id}_viewed'] = True
    
    # Get related videos from the same subject
    related_videos = video.subject.videos.exclude(id=video_id).order_by('-upload_date')[:5]
    
    # Calculate statistics
    unique_viewers = Video.objects.filter(id=video_id).aggregate(
        unique_viewers=Count('views', filter=Q(views__gt=0))
    )['unique_viewers']
    
    avg_watch_time = video.duration / 60 if video.duration else 0  # Convert to minutes

    context = {
        'video': video,
        'related_videos': related_videos,
        'unique_viewers': unique_viewers,
        'avg_watch_time': avg_watch_time
    }
    return render(request, 'core/video_detail.html', context)

@login_required
def search_view(request):
    subjects = Subject.objects.filter(created_by=request.user)
    query = request.GET.get('q', '')
    subject_id = request.GET.get('subject', '')
    
    # Start with all videos that belong to subjects created by the user
    videos = Video.objects.filter(subject__created_by=request.user)
    
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    if subject_id and subject_id.isdigit():
        videos = videos.filter(subject_id=int(subject_id))
    
    videos = videos.select_related('subject').order_by('-upload_date')
    
    context = {
        'subjects': subjects,
        'videos': videos,
        'query': query,
        'selected_subject': subject_id,
        'debug_info': {
            'subject_count': subjects.count(),
            'subject_names': [s.name for s in subjects],
            'video_count': videos.count(),
        }
    }
    return render(request, 'core/search.html', context)

@login_required
def video_upload_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        subject_id = request.POST.get('subject')
        duration = int(request.POST.get('duration')) * 60  # Convert minutes to seconds
        
        video = Video.objects.create(
            title=title,
            description=description,
            url=url,
            subject_id=subject_id,
            duration=duration,
            uploaded_by=request.user
        )
        
        messages.success(request, 'Video uploaded successfully!')
        return redirect('video_detail', video_id=video.id)
    
    subjects = Subject.objects.filter(created_by=request.user)
    return render(request, 'core/video_upload.html', {'subjects': subjects})

@login_required
def toggle_topic_completion(request, topic_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
    
    try:
        data = json.loads(request.body)
        is_completed = data.get('is_completed', False)
        
        topic = get_object_or_404(Topic, id=topic_id)
        progress, created = TopicProgress.objects.get_or_create(
            topic=topic,
            user=request.user,
            defaults={'is_completed': is_completed}
        )
        
        if not created:
            progress.is_completed = is_completed
            if is_completed:
                progress.completed_at = timezone.now()
            progress.save()
        
        return JsonResponse({
            'success': True,
            'is_completed': progress.is_completed,
            'completed_at': progress.completed_at.isoformat() if progress.completed_at else None
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def add_video_to_topic(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
    
    try:
        topic_id = request.POST.get('topic_id')
        url = request.POST.get('url')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        duration = int(request.POST.get('duration', 0)) * 60  # Convert minutes to seconds
        
        topic = get_object_or_404(Topic, id=topic_id)
        
        # Create the video
        video = Video.objects.create(
            title=title,
            description=description,
            url=url,
            duration=duration,
            subject=topic.subject,
            uploaded_by=request.user
        )
        
        # Add the video to the topic
        topic.videos.add(video)
        
        messages.success(request, 'Video added successfully!')
        return redirect('subject_detail', subject_id=topic.subject.id)
        
    except Exception as e:
        messages.error(request, f'Error adding video: {str(e)}')
        return redirect('subject_detail', subject_id=topic.subject.id)
