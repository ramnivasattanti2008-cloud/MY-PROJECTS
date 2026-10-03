from django.contrib import admin
from .models import Profile, Post, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'website', 'created_at']
    search_fields = ['user__username', 'bio', 'location']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'created_at', 'like_count_display')
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def like_count_display(self, obj):
        return obj.like_count
    like_count_display.short_description = 'Likes'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
