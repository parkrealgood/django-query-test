from rest_framework import serializers
from django.db import transaction

from ticket.models import UserTicket, TicketSerialGenerator


class UserTicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTicket
        fields = '__all__'


class UserTicketCreateSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(label='Post ID')
    user_id = serializers.IntegerField(label='User ID')

    @transaction.atomic()
    def create(self, validated_data):
        """
        티켓 생성
        :param validated_data: {Post ID, User ID}
        :return: User Ticket 객체
        """
        ticket_serial = TicketSerialGenerator.generate_ticket_serial()
        ticket = UserTicket.objects.create(
            post_id=validated_data['post_id'],
            user_id=validated_data['user_id'],
            ticket_serial=ticket_serial,
            is_expired=False
        )
        return ticket
