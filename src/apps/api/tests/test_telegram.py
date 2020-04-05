from collections import namedtuple
from io import BytesIO
from unittest.mock import patch

import requests

from apps.about.models import Discount
from apps.api.impl.v1.views import TelegramView
from apps.api.tests.base import ApiTest


class Test(ApiTest):
    def setUp(self):
        self.__create_discounts()

    @patch.object(TelegramView, TelegramView.download_photo.__name__)
    def test_get_captions_kfc(self, mock_download_photo):
        mock_download_photo.return_value = "xxx"

        view = TelegramView()
        captions = view.get_captions_kfc()
        self.assertEqual(len(captions), 4)
        self.assertEqual(captions, [("KFC", "xxx")] * 4)

    @patch.object(TelegramView, TelegramView.download_photo.__name__)
    def test_get_captions_korona(self, mock_download_photo):
        mock_download_photo.return_value = "xxx"

        view = TelegramView()
        captions = view.get_captions_korona()
        self.assertEqual(len(captions), 4)
        self.assertEqual(
            captions,
            [
                ("Korona", "name_of_discount_1", "xxx", "text_1_Korona"),
                ("Korona", "name_of_discount_2", "xxx", "text_2_Korona"),
                ("Korona", "name_of_discount_3", "xxx", "text_3_Korona"),
                ("Korona", "name_of_discount_4", "xxx", "text_4_Korona"),
            ],
        )

    @patch.object(TelegramView, TelegramView.download_photo.__name__)
    def test_get_captions_evroopt(self, mock_download_photo):
        mock_download_photo.return_value = "xxx"

        view = TelegramView()
        captions = view.get_captions_evroopt()
        self.assertEqual(len(captions), 4)
        self.assertEqual(
            captions,
            [
                ("Evroopt", "name_of_discount_1", "xxx"),
                ("Evroopt", "name_of_discount_2", "xxx"),
                ("Evroopt", "name_of_discount_3", "xxx"),
                ("Evroopt", "name_of_discount_4", "xxx"),
            ],
        )

    @patch.object(requests, requests.get.__name__)
    def test_download_photo(self, mock_requests_get):
        mock_requests_get.return_value = namedtuple("_", ["content"])(b"0123")

        view = TelegramView()
        photo = view.download_photo("lol url")

        mock_requests_get.assert_called_with("lol url")
        self.assertIsInstance(photo, BytesIO)
        self.assertEqual(photo.tell(), 0)
        self.assertEqual(photo.read(), b"0123")

    @patch.object(requests, requests.post.__name__)
    def test_bot_respond(self, mock_requests_post):
        mock_requests_post.return_value = "lol resp"

        view = TelegramView()

        resp = view.bot_respond({"id": "lol chat id"})

        mock_requests_post.assert_called_with(
            "https://api.telegram.org/botbot/sendMessage",
            json={
                "chat_id": "lol chat id",
                "reply_markup": {
                    "keyboard": [
                        [{"text": "KFC"}],
                        [{"text": "Evroopt"}],
                        [{"text": "Korona"}],
                    ],
                    "resize_keyboard": True,
                },
            },
        )

        self.assertEqual(resp, "lol resp")

    @patch.object(requests, requests.post.__name__)
    def test_bot_respond_with_photo_kfc(self, mock_requests_post):
        mock_requests_post.return_value = "lol resp"

        view = TelegramView()

        resp = view.bot_respond_with_photo_kfc({"id": "lol chat id"}, "xy")

        mock_requests_post.assert_called_with(
            "https://api.telegram.org/botbot/sendPhoto",
            data={"chat_id": "lol chat id", "caption": "x"},
            files={"photo": ("InputFile", "y")},
        )

        self.assertEqual(resp, "lol resp")

    @patch.object(requests, requests.post.__name__)
    def test_bot_respond_with_photo_korona(self, mock_requests_post):
        mock_requests_post.return_value = "lol resp"

        view = TelegramView()

        resp = view.bot_respond_with_photo_korona({"id": "lol chat id"}, "xyz")

        mock_requests_post.assert_called_with(
            "https://api.telegram.org/botbot/sendPhoto",
            data={"chat_id": "lol chat id", "caption": "x"},
            files={"photo": ("InputFile", "z")},
        )

        self.assertEqual(resp, "lol resp")

    @patch.object(requests, requests.post.__name__)
    def test_bot_respond_with_photo_evroopt(self, mock_requests_post):
        mock_requests_post.return_value = "lol resp"

        view = TelegramView()

        resp = view.bot_respond_with_photo_evroopt({"id": "lol chat id"}, "xyz")

        mock_requests_post.assert_called_with(
            "https://api.telegram.org/botbot/sendPhoto",
            data={"chat_id": "lol chat id", "caption": "x"},
            files={"photo": ("InputFile", "z")},
        )

        self.assertEqual(resp, "lol resp")

    @staticmethod
    def __create_discounts():
        nr_discount_per_shop = 4
        shops = {"KFC", "Korona", "Evroopt"}

        for shop in shops:
            for i in range(1, nr_discount_per_shop + 1):
                dsc = Discount(
                    name_of_discount=f"name_of_discount_{i}",
                    media=f"media_{i}",
                    shop=shop,
                    text=f"text_{i}_{shop}",
                )
                dsc.save()
