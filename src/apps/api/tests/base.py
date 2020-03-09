import os
from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from apps.api.models.api_settings import ApiSettings
from apps.about.models.post_kateg import Post_kateg
from apps.about.models.katalog import Katalog
from apps.about.models.post import Post
from apps.about.models.discount import Discount

User = get_user_model()


class ApiTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_user(
            "testadmin", "testadmin@test.com", "testadminpassword"
        )
        self.admin.is_superuser = True
        self.admin.is_staff = True
        self.admin.save()
        self.admin_token = os.urandom(8).hex()

        api_settings = ApiSettings(user=self.admin, token=self.admin_token)
        api_settings.save()

        self.user = User.objects.create_user("test", "test@test.com", "testpassword")
        self.user_token = os.urandom(8).hex()

        api_settings = ApiSettings(user=self.user, token=self.user_token)
        api_settings.save()

    def create_post_kateg(self, name) -> Post_kateg:
        post_kateg = Post_kateg(name=name)
        post_kateg.save()

        return post_kateg

    def create_post(self,title, content, media,  at: date, post_kateg: Post_kateg) -> Post:
        post = Post(title=title, content=content, media=media, at=at, post_kateg= post_kateg)
        post.save()

        return post

    def create_discount(self, media,shop) -> Discount:
        discount = Discount(media=media, shop=shop)
        discount.save()

        return discount

    def create_katalog(self, title,content, media, adress) -> Katalog:
        katalog = Katalog(title=title, content=content, media=media, adress=adress)
        katalog.save()

        return katalog
