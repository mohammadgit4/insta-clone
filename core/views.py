from .models import Follow, Post, Like, Comment
from rest_framework.response import Response
from .serializers import CommentSLR, FollowerSLR, PostSLR, LikeSLR
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# Post View
class PostView(GenericAPIView):
    serializer_class = PostSLR
    permisson_classes = (IsAuthenticated,)
    def get(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response({'message':'First Log in Your Account'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if pk is not None:
                data =  Post.objects.get(id=pk, user=self.request.user)
                slr = self.serializer_class(data)
                return Response({'message':'Get one data', 'data':slr.data}, status=status.HTTP_200_OK)
            data = Post.objects.filter(user=self.request.user)
            slr = self.serializer_class(data, many=True)
            return Response({'message':'Get all data', 'data':slr.data}, status=status.HTTP_200_OK)

    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'request':request})
        slr.is_valid(raise_exception=True)
        slr.save()
        return Response({'message':'Data Created...', 'data':slr.data}, status=status.HTTP_201_CREATED)

    def patch(self, request, pk=None):
        data = Post.objects.get(id=pk, user=request.user)
        slr = self.serializer_class(data, data=request.data, context={'request':request}, partial=True)
        slr.is_valid(raise_exception=True)
        slr.save()
        return Response({'message':'Update data Successfully', 'data':slr.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        Post.objects.get(id=pk, user=request.user).delete()
        return Response({'message':'Data Deleted....'}, status=status.HTTP_204_NO_CONTENT)

# This one is Clss View
class LikeView(GenericAPIView):
    serializer_class = LikeSLR
    permission_class = (IsAuthenticated,)

    def post(self, request, pk=None):
        slr = self.serializer_class(data=request.data, context={'request':request})
        slr.is_valid(raise_exception=True)
        slr.save()
        return Response({'message':"Liked!"}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        instance = Like.objects.get(id=pk, user=self.request.user)
        instance.delete()
        return Response({'message':"Disliked!"}, status=status.HTTP_204_NO_CONTENT)

# This one is Comment View
class CommentView(GenericAPIView):
    serializer_class = CommentSLR
    permission_class = (IsAuthenticated,)

    def patch(self, request, pk=None):
        if pk is not None:
            data = Comment.objects.get(id=pk, user=self.request.user)
            slr = self.serializer_class(data, data=self.request.data, context={'request':request}, partial=True)
            slr.is_valid(raise_exception=True)
            slr.save()
            return Response({'message':'Comment Updated !', 'data':slr.data}, status=status.HTTP_200_OK)
        slr = self.serializer_class(data=self.request.data, context={'request':request})
        slr.is_valid(raise_exception=True)
        slr.save()
        return Response({'message':'Comment Posted !', 'data':slr.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        instance = Comment.objects.get(id=pk, user=self.request.user)
        instance.delete()
        return Response({'message':'Data Deleted!'}, status=status.HTTP_204_NO_CONTENT)

class FollowsView(GenericAPIView):
    serializer_class = FollowerSLR
    permission_class = (IsAuthenticated,)
    def get(self, request):
        following = Follower.objects.filter(user=request.user)
        slr = self.serializer_class(following, many=True)
        return Response({'message':'All followed list', 'data':slr.data}, status=status.HTTP_200_OK)

    def post(self, request):
        slr = self.serializer_class(data=request.data, context={'request':request})
        slr.is_valid(raise_exception=True)
        slr.save()
        return Response({'message':'Followed', 'data':slr.data}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk=None):
        instance = Follower.objects.get(id=pk, user=self.request.user)
        instance.delete()
        return Response({'message':'Unfollowed!'}, status=status.HTTP_204_NO_CONTENT)

class getFollowers(RetrieveAPIView):
    serializer_class = FollowerSLR
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        followers = Follow.objects.filter(follower=request.user)
        slr = self.serializer_class(followers, many=True)
        return Response({'message':'All followed list', 'data':slr.data}, status=status.HTTP_200_OK)