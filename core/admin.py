from django.contrib import admin
from .models import Post, Comment, Like, Follow

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'comment', 'commented_on', 'updated_at')

@admin.register(Like)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'liked_at', 'updated_at')

@admin.register(Follow)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follower', 'followed_on', 'updated_at')