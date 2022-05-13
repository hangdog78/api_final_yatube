from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import GroupViewSet, PostViewSet, CommentsViewSet, FollowViewSet

api_v1_router = routers.DefaultRouter()

api_v1_router.register(r'posts/(?P<post_id>\d+)/comments',
                       CommentsViewSet,
                       basename='comments'
                       )
api_v1_router.register('posts', PostViewSet)
api_v1_router.register('groups', GroupViewSet)
api_v1_router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]