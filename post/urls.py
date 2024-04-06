from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet

router = routers.DefaultRouter()
router.register('', PostViewSet, basename='post')

urlpatterns = [
    path('post/', include(router.urls)),
]
