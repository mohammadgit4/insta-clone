from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    post = models.ImageField(upload_to='insta_post')
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post {self.pk}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower_id', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)