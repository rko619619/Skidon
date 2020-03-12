from rest_framework import status
from datetime import date

from apps.api.tests.base import ApiTest


class PostApiTest(ApiTest):
    def test_read(self):
        at1 = date(year=2019, month=2, day=14)
        post_kateg1 = self.create_post_kateg("post_kateg1")
        ph1 = self.create_post(name="name1", at=at1, post_kateg=post_kateg1)

        at2 = date(year=2019, month=3, day=15)
        ph2 = self.create_post(name="name2", at=at2, post_kateg=post_kateg1)

        headers = {"HTTP_AUTHORIZATION": self.admin_token}
        response = self.client.get("/api/v1/post/", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, ph in zip(payload, (ph1, ph2)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj,
                {
                    "id": ph.pk,
                    "title": ph.title,
                    "content": ph.content,
                    "media": ph.media,
                    "at": ph.at.strftime("%Y-%m-%d"),
                    "post_kateg": post_kateg1.pk,
                },
            )

    def test_retrieve(self):

        at1 = date(year=2019, month=2, day=14)
        ph = self.create_post(name="title", at=at1, post_kateg="post_kateg1")

        response = self.client.get(f"/api/v1/post/{ph.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload,
            {
                "id": ph.pk,
                "title": ph.media,
                "content": ph.content,
                "media": ph.media,
                "at": ph.at.strftime("%Y-%m-%d"),
                "post_kateg": ph.post_kateg,
            },
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content": "content",
            "media": "media",
            "at": "at",
            "post_kateg": "post_kateg",
        }

        response = self.client.post("/api/v1/post/", data=data, **user_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/api/v1/post/", data=data, **admin_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        at1 = date(year=2019, month=2, day=14)
        post_kateg1 = self.create_post_kateg("post_kateg1")
        ph1 = self.create_post(name="name1", at=at1, post_kateg=post_kateg1)

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content": "content",
            "media": "media",
            "st": "st",
            "post_kateg": "post_kateg",
        }

        response = self.client.put(
            f"/api/v1/post/{ph1.pk}/", data=data,content_type="application/json", **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post/{ph1.pk}/",content_type="application/json", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/post/{ph1.pk}/", data=data,content_type="application/json", **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post/{ph1.pk}/", data=data,content_type="application/json", **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        at1 = date(year=2019, month=2, day=14)
        post_kateg1 = self.create_post_kateg("post_kateg1")
        ph1 = self.create_post(name="name1", at=at1, post_kateg=post_kateg1)

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content": "content",
            "media": "media",
            "at": "at",
            "post_kateg": "post_kateg",
        }

        response = self.client.delete(f"/api/v1/post/{ph1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(f"/api/v1/post/{ph1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
