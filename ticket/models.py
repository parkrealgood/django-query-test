import random
import string
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

from core.models import TimeStampModel


class TicketSerialGenerator(TimeStampModel):
    ticket_serial = models.CharField(primary_key=True, max_length=12, verbose_name='티켓 시리얼 번호')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = models.Manager()

    class Meta:
        verbose_name = '티켓 번호 생성기'
        verbose_name_plural = '티켓 번호 생성기 목록'
        constraints = [
            models.UniqueConstraint(fields=['uuid'], name='unique_uuid')
        ]
        indexes = [
            models.Index(fields=['uuid'])
        ]

    @classmethod
    def generate_ticket_serial(cls) -> str:
        """
        티켓 시리얼 번호 생성
        :return: 시리얼번호
        """
        current_date = localtime().now()
        year = str(current_date.year)[-2:]
        month = str(current_date.month).zfill(2)
        day = str(current_date.day).zfill(2)
        postfix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        ticket_serial = f'{year}{month}{day}{postfix}'
        try:
            generator = TicketSerialGenerator.objects.get(ticket_serial=ticket_serial)
            if generator:
                TicketSerialGenerator.generate_ticket_serial()
        except:
            TicketSerialGenerator.objects.create(ticket_serial=ticket_serial)
        return ticket_serial


class UserTicket(TimeStampModel):
    post = models.ForeignKey(
        'post.Post', on_delete=models.CASCADE, related_name='post_tickets', verbose_name='게시글'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', verbose_name='유저')
    ticket_serial = models.CharField(max_length=12, verbose_name='티켓 시리얼 번호')
    is_expired = models.BooleanField(default=True, verbose_name='만료여부')

    objects = models.Manager()

    class Meta:
        ordering = ['-id']
        verbose_name = '티켓'
        verbose_name_plural = '티켓 목록'
        constraints = [
            models.UniqueConstraint(fields=['ticket_serial'], name='unique_post_user')
        ]

    def __str__(self):
        return f'{self.user}'
