from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post, User
from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AllButAuthorReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AllButAuthorReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        group=Group.objects.filter(
                            id=self.request.data.get("group")).first()
                        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        following_name = self.request.data.get("following", None)

        if following_name is None:
            raise ParseError(detail='following - Обязательное поле.', code=400)

        following = get_object_or_404(User, username=following_name)

        if self.request.user == following:
            raise ParseError(detail='Невозможно подписаться на себя.',
                             code=400)

        if Follow.objects.filter(user=self.request.user,
                                 following=following).exists():
            raise ParseError(detail='Уже пподписан.', code=400)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, following=following)
