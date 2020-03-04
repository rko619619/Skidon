import json

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.views.generic import View

from dynaconf import settings
from django.http.response import JsonResponse
import requests


class TelegramView(View):
    def post(self, request: HttpRequest, *_args, **_kw):
        if not settings.TELEGRAM_SKIDON_TOKEN:
            raise PermissionDenied("no bot token")
        payload = json.loads(request.body)

        message = payload["message"]
        chat_id = message["chat"]["id"]
        user_id = message["from"]["id"]
        last_name = message["from"]["last_name"]

        tg_url = f"https://api.telegram.org/bot{settings.TELEGRAM_SKIDON_TOKEN}/sendMessage"
        tg_resp = requests.post(
            tg_url, json={"chat_id": chat_id, "text": last_name}
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
