from rest_framework import status
from datetime import date

from apps.api.tests.base import ApiTest


class PostApiTest(ApiTest):
    def test_read(self):
        at1 = date(year=2019, month=2, day=14)
        post_kateg = self.create_post_kateg("post_kateg")
        ph1 = self.create_post(
            name="name", content="content", media="media", at=at1, post_kateg=post_kateg
        )

        headers = {"HTTP_AUTHORIZATION": self.admin_token}
        response = self.client.get("/api/v1/post/", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, ph in zip(payload, (ph2, ph1)):
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
                    "post_kateg": post_kateg.pk,
                },
            )

    def test_retrieve(self):
        title = self.create_post("title")

        response = self.client.get(f"/api/v1/post/{title.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload,
            {
                "id": title.pk,
                "title": title.media,
                "content": title.content,
                "media": title.media,
                "st": title.at,
                "post_kateg": title.post_kateg,
            },
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content": "content",
            "media": "media",
            "st": "st",
            "post_kateg": "post_kateg",
        }

        response = self.client.post("/api/v1/post/", data=data, **user_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post("/api/v1/post/", data=data, **admin_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        title = self.create_post("title")

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
            f"/api/v1/post/{title.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post/{title.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/post/{title.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post/{title.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        title = self.create_post("title")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content": "content",
            "media": "media",
            "st": "st",
            "post_kateg": "post_kateg",
        }

        response = self.client.delete(
            f"/api/v1/post/{title.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(
            f"/api/v1/post/{title.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
