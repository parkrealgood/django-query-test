from django.db import models

from core.models import TimeStampModel


class Post(TimeStampModel):
    title = models.CharField(max_length=255, verbose_name='제목')
    content = models.TextField(verbose_name='내용')

    objects = models.Manager()

    class Meta:
        ordering = ['-id']
        verbose_name = '게시글'

    def __str__(self):
        return self.title


class Subscriber(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='subscribers', verbose_name='게시글')
    name = models.CharField(max_length=255, verbose_name='이름')

    objects = models.Manager()

    class Meta:
        ordering = ['-id']
        verbose_name = '게시글 구독자'

    def __str__(self):
        return self.name


class SubscriberFollower(TimeStampModel):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='followers', verbose_name='구독자')
    name = models.CharField(max_length=255, verbose_name='이름')

    objects = models.Manager()

    class Meta:
        ordering = ['-id']
        verbose_name = '구독자 팔로워'

    def __str__(self):
        return self.name
