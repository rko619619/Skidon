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
from apps.api.impl.v1.serializers import Post_kategSerializer
from apps.api.impl.v1.serializers import PostSerializer


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
            print("Good")
        except Exception as err:
            print("ERROR!!!!!!!", err)
            ok = False

        return Response(data={"ok": ok}, content_type="application/json")

    def _do_post(self, request):
        kw = {}
        bot_response = ""
        if "message" not in request.data:
            return False
        message = request.data["message"]
        chat = message["chat"]
        user = message["from"]
        text = message.get("text")
        if not text:
            return False
        if text == "\start":
            if user.get("username"):
                bot_response += "@" + user["username"]
            elif user.get("first_name"):
                bot_response += user["first_name"]
                if user.get("last_name"):
                    bot_response += " " + user["last_name"]
            bot_response += ", привет! Ты попал на Скидон бота! Все самые жаркие и актуальные скидки только здесь. Заходи, пользуйся, все в твоих руках.\nМожешь выбирать скидон и погнали :)"
            kw["message_id"] = message["message_id"]

        elif text == "KFC":
            captions = self.get_captions_group(text)
            self.transform(captions, chat)

        elif text == "Хит":
            text = "Hit"
            captions = self.get_captions_group(text)
            self.transform(captions, chat)

        elif text == "Гиппо":
            text = "Gippo"
            captions = self.get_captions_group(text)
            self.transform(captions, chat)

        elif text == "Евроопт":
            text = "Evroopt"
            captions = self.get_captions_group(text)
            self.transform(captions, chat)

        elif text == "Корона":
            captions = self.get_captions_korona()
            for caption in captions:
                tg = self.bot_respond_with_photo_korona(chat, caption)
                print(tg)

        elif text == "Виталюр":
            captions = self.get_captions_vitalur()
            for caption in captions:
                tg = self.bot_respond_with_photo_vitalur(chat, caption)
                print(tg)

        else:
            if user.get("username"):
                bot_response += "@" + user["username"]
            elif user.get("first_name"):
                bot_response += user["first_name"]
                if user.get("last_name"):
                    bot_response += " " + user["last_name"]
            bot_response += ". Попробуй что-то другое!"
            kw["message_id"] = message["message_id"]
        self.bot_respond(chat, bot_response, **kw)

        return True

    def get_captions_group(self, text):
        discounts = Discount.objects.filter(shop=f"{text}")

        discounts_post = []

        for dis in discounts:
            photo_url = dis.media
            discounts_post.append(photo_url)
        return discounts_post

    def get_captions_korona(self):
        discounts = Discount.objects.filter(shop="Korona")

        discounts_post = []

        for dis in discounts[0:20:]:
            shop = dis.shop
            name_of_discount = dis.name_of_discount
            photo = self.download_photo(dis.media)
            text = dis.text
            discounts_post.append((shop, name_of_discount, photo, text))
        return discounts_post

    def get_captions_vitalur(self):
        discounts = Discount.objects.filter(shop="Vitalur")

        discounts_post = []

        for dis in discounts[0:20:]:
            shop = dis.shop
            text = dis.text
            name_of_discount = dis.name_of_discount
            photo = self.download_photo(dis.media)
            price = dis.price.replace("\n", ".").replace(" ", ".")
            discounts_post.append((shop, text, name_of_discount, photo, price))
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
                    [{"text": "KFC"}],
                    [{"text": "Виталюр"}, {"text": "Гиппо"}],
                    [{"text": "Евроопт"}, {"text": "Корона"}, {"text": "Хит"}],
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

    def transform(self, captions, chat):

        photos = []
        for caption in captions:
            photos.append(caption)
            if photos.__len__() == 10:
                tg = self.bot_respond_with_photo_group(chat, photos)
                print(tg)
                photos.clear()
        if photos.__len__() != 0:
            tg = self.bot_respond_with_photo_group(chat, photos)
            print(tg)
            photos.clear()

    def bot_respond_with_photo_group(self, chat, caption):

        bot_url = f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDONBOT_TOKEN}/sendMediaGroup"

        media = []
        i = 0
        for photo in caption:
            i += 1
            new_photo = {"type": "photo", "media": f"{photo}"}

            media.append(new_photo)
            if i == 10:
                break

        body = {"chat_id": chat["id"], "media": media}

        resp = requests.post(bot_url, json=body)

        return resp

    def bot_respond_with_photo_korona(self, chat, caption):
        bot_url = (
            f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDONBOT_TOKEN}/sendPhoto"
        )

        payload = {
            "chat_id": chat["id"],
            "caption": f"{caption[0]}\n{caption[1]}\n{caption[3]}",
        }

        files = {"photo": ("InputFile", caption[2])}

        tg_resp = requests.post(bot_url, data=payload, files=files)

        return tg_resp

    def bot_respond_with_photo_vitalur(self, chat, caption):
        bot_url = (
            f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDONBOT_TOKEN}/sendPhoto"
        )

        payload = {
            "chat_id": chat["id"],
            "caption": f"{caption[0]}\n{caption[1]}\n{caption[2]}\n{caption[4]}",
        }

        files = {"photo": ("InputFile", caption[3])}

        tg_resp = requests.post(bot_url, data=payload, files=files)

        return tg_resp
