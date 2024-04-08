from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ticket.models import UserTicket
from ticket.serializers import UserTicketListSerializer, UserTicketCreateSerializer


class TicketViewSet(GenericViewSet):
    """
    Post 관련 API ViewSet
    """
    serializer_class = UserTicketListSerializer
    permission_classes = (AllowAny,)
    queryset = UserTicket.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserTicketCreateSerializer
        return UserTicketListSerializer

    def list(self, request, *args, **kwargs):
        """
        Ticket 목록 조회
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Ticket 상세 조회
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Ticket 생성
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
