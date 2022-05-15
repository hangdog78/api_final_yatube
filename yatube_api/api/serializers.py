from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = PrimaryKeyRelatedField(many=False,
                                   read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True,
                            slug_field='username')
    following = SlugRelatedField(read_only=True,
                                 slug_field='username')

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        user = self.context['request'].user
        following_name = self.context['request'].data.get('following')

        if following_name is None:
            raise serializers.ValidationError('following - Обязательное поле.',
                                              code=400)

        following = get_object_or_404(User, username=following_name)

        if user == following:
            raise serializers.ValidationError(
                'Невозможно подписаться на себя.',
                code=400)

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError('Уже подписан.', code=400)

        data['user'] = user
        data['following'] = following
        return data
