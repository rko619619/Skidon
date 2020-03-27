import io

import requests
from dynaconf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.about.models import Discount
from apps.about.models import Katalog
from apps.about.models import Post
from apps.about.models import Post_kateg
from apps.api.impl.v1.serializers import DiscountSerializer
from apps.api.impl.v1.serializers import KatalogSerializer
from apps.api.impl.v1.serializers import PostSerializer
from apps.api.impl.v1.serializers import Post_kategSerializer


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
        except Exception as err:
            print("ERROR!!!!!!!", err)
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

        if text in ("", "Актуальные"):
            captions = self.get_captions()
            for caption in captions:
                self.bot_respond_with_photo(chat, caption)

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
        tg_resp = self.bot_respond(chat, bot_response, **kw)
        print(tg_resp)
        return True

    def get_captions(self):
        discounts = Discount.objects.all()

        discounts_post = []

        for dis in discounts:
            shop = dis.shop
            photo = self.download_photo(dis.media)
            discounts_post.append((shop, photo))
        return discounts_post

    def download_photo(self, file_url):

        response = requests.get(file_url)

        image = io.BytesIO()
        image.write(response.content)
        image.seek(0)

        return image

    def bot_respond(self, chat, reply, message_id=None, html=False):
        bot_url = f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDONBOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat["id"],
            "text": reply,
            "reply_markup": {
                "keyboard": [
                    [{"text": "Скидки"}],
                    [{"text": "Новости о еде"}],
                    [{"text": "Следуюшая"}, {"text": "Предыдущая"}],
                ],
                "resize_keyboard": True,
            },
        }

        if html:
            payload["parse_mode"] = "HTML"

        if message_id:
            payload["reply_to_message_id"] = message_id

        tg_resp = requests.post(bot_url, json=payload)

        return tg_resp

    def bot_respond_with_photo(self, chat, caption):
        bot_url = f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDONBOT_TOKEN}/sendPhoto"

        payload = {
            "chat_id": chat["id"],
            "caption": caption[0],
        }

        files = {"photo": ("InputFile", caption[1])}

        tg_resp = requests.post(bot_url, data=payload, files=files)

        return tg_resp
