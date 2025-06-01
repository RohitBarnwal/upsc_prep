from django.db import models
from .subject import Subject
from .user import User
from .video import Video

class Topic(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    videos = models.ManyToManyField(Video, related_name='topics', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['subject', 'order', 'name']
        unique_together = ['subject', 'name']

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class TopicProgress(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['topic', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.topic.name} - {'Completed' if self.is_completed else 'In Progress'}" 