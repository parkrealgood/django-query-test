from django.urls import path, include
from rest_framework import routers

from ticket.views import TicketViewSet

router = routers.DefaultRouter()
router.register('', TicketViewSet, basename='ticket')

urlpatterns = [
    path('ticket/', include(router.urls)),
]
