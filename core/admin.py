from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, Video

admin.site.register(User, UserAdmin)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'upload_date', 'views', 'is_active')
    list_filter = ('subject', 'is_active', 'upload_date')
    search_fields = ('title', 'description')
    readonly_fields = ('views',)
