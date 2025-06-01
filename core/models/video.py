from django.db import models
from django.utils import timezone
from .user import User
from .subject import Subject
import re

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_videos')
    upload_date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(help_text="Duration in seconds", null=True, blank=True)
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Convert YouTube watch URLs to embed URLs
        youtube_pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([^\s&]+)'
        match = re.match(youtube_pattern, self.url)
        if match:
            video_id = match.group(1)
            self.url = f'https://www.youtube.com/embed/{video_id}'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-upload_date'] 