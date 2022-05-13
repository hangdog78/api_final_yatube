from django.shortcuts import get_object_or_404
from posts.models import Group, Post, Follow, Comment
from rest_framework import viewsets, permissions

from .permissions import AllButAuthorReadOnly
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllButAuthorReadOnly,)

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = (AllButAuthorReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user,
                        post=post)


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
