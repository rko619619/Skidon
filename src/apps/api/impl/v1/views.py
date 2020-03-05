import requests
from datetime import date
from datetime import datetime
from dynaconf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from apps.about.models import Discount, Katalog, Post_kateg, Post

from apps.api.impl.v1.serializers import (
    DiscountSerializer,
    KatalogSerializer,
    Post_kategSerializer,
    PostSerializer,
)


class DiscountViewSet(ReadOnlyModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class KatalogViewSet(ReadOnlyModelViewSet):
    queryset = Katalog.objects.all()
    serializer_class = KatalogSerializer


class Post_kategViewSet(ReadOnlyModelViewSet):
    queryset = Post_kateg.objects.all()
    serializer_class = Post_kategSerializer


class PostViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = PostSerializer
    lookup_field = "post_kateg"
    queryset = Post.objects.all()

class TelegramView(APIView):
    def post(self, request: Request, *_args, **_kw):
        if not settings.TELEGRAM_SKIDON_TOKEN:
            raise PermissionDenied("no bot token")
        message= requests.data["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        last_name = message["from"]["last_name"]

        tg_url = (
            f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDON_TOKEN}/sendMessage"
        )
        tg_resp = requests.post(tg_url, json={"chat_id": chat_id, "text": last_name})

        return Response(
            data={
                "chat_id": chat_id,
                "message": message,
                "tg": str(tg_resp),
                "user_id": user_id,
            },
            # content_type="application/json",
        )
