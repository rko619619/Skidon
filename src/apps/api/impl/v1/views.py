import requests
from dynaconf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from apps.about.models import Discount, Katalog, Post_kateg, Post

from apps.api.impl.v1.serializers import (
    DiscountSerializer,
    KatalogSerializer,
    Post_kategSerializer,
    PostSerializer,
)


class DiscountViewSet(ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class KatalogViewSet(ModelViewSet):
    queryset = Katalog.objects.all()
    serializer_class = KatalogSerializer


class Post_kategViewSet(ModelViewSet):
    queryset = Post_kateg.objects.all()
    serializer_class = Post_kategSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class TelegramView(APIView):
    def post(self, request: Request, *_args, **_kw):
        if not settings.TELEGRAM_SKIDONBOT_TOKEN or not request:
            raise PermissionDenied("invalid bot configuration")

        try:
            ok = self._do_post(request)
        except Exception:
            ok = False

        return Response(data={"ok": ok}, content_type="application/json")

    def _do_post(self, request):
        if "message" not in request.data:
            return False
        message = request.data["message"]
        chat = message["chat"]
        user = message["from"]
        text = message.get("text")
        if not text:
            return False
        kw = {}

        if text in ("/actual", "Актуальные"):
            bot_response = "Актуальные цены:\n\n" + "\n".join(self.get_actual_prices())
        else:
            bot_response = ""
            if user.get("username"):
                bot_response += "@" + user["username"]
            elif user.get("first_name"):
                bot_response += user["first_name"]
                if user.get("last_name"):
                    bot_response += " " + user["last_name"]

            bot_response += "! За слова ответишь?"
            kw["message_id"] = message["message_id"]

        return True

    def get_actual_prices(self):
        discounts = Discount.objects.all()

        discounts_post = []


        for dis in discounts:
            discount = f"{discounts.media}: {discounts.shop}"
            discount.append(discounts_post)

        return discounts_post