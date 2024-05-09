from django.db.models import Prefetch, Subquery, OuterRef
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from post.models import Post, Subscriber, SubscriberFollower
from post.serializers import PostRetrieveSerializer


class PostViewSet(GenericViewSet):
    """
    Post 관련 API ViewSet
    """
    serializer_class = PostRetrieveSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Post.objects.prefetch_related(
            Prefetch(
                'subscribers',
                queryset=Subscriber.objects.prefetch_related(
                    Prefetch(
                        'followers',
                        queryset=SubscriberFollower.objects.filter(),
                        to_attr='prefetch_followers'
                    )
                ),
                to_attr='prefetch_subscribers'
            )
        ).annotate(
            first_subscriber_name=Subquery(
                Subscriber.objects.filter(post=OuterRef('pk')).values('name')[:1]
            ),
            first_subscriber_follower_name=Subquery(
                SubscriberFollower.objects.filter(subscriber=OuterRef('subscribers')).values('name')[:1]
            )
        )
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Post 목록 조회
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Post 상세 조회
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
