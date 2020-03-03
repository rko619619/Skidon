import json

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.views.generic import View

from dynaconf import settings
from urllib.request import Request
from django.http.response import JsonResponse
import requests


class TelegramView(View):
    def post(self, request: HttpRequest, *_args, **_kw):
        if not settings.TELEGRAM_SKIDONBOT_TOKEN:
            raise PermissionDenied("no bot token")
        payload = json.loads(request.body)

        message = payload["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]

        tg_url = f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDONBOT_TOKEN}/sendMessage"
        tg_resp = requests.post(
            tg_url, json={"chat_id": chat_id, "text": payload}
        )

        return JsonResponse(
            data={
                "chat_id": chat_id,
                "message": message,
                "tg": str(tg_resp),
                "user_id": user_id,
            },
            # content_type="application/json",
        )
