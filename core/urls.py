from django.urls import path
from .views import PostView, LikeView, CommentView, FollowsView, getFollowers


urlpatterns = [
    path('', PostView.as_view(), name='addandshow'),
    path('<int:pk>/', PostView.as_view()),
    path('like/', LikeView.as_view(), name='like'),
    path('unlike/<int:pk>/', LikeView.as_view(), name='unlike'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('comment/<int:pk>/', CommentView.as_view(), name='updatecomment'),
    path('follow/', FollowsView.as_view(), name='follow'),
    path('followed/', FollowsView.as_view(), name='followed'),
    path('unfollow/<int:pk>/', FollowsView.as_view(), name='unfollow'),
    path('getfollowers/', getFollowers.as_view(), name='getfollowers')
]