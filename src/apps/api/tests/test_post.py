from datetime import date
from typing import Optional

from rest_framework import status

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
        post_kateg1 = self.create_post_kateg("post_kateg")
        ph = self.create_post(name="title", at=at1, post_kateg=post_kateg1)

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
                "post_kateg": ph.post_kateg.pk,
            },
        )

    def test_create(self):
        at1 = date(year=2019, month=2, day=14)
        post_kateg1 = self.create_post_kateg("post_kateg1")
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data1 = {
            "at": at1,
            "content": "content",
            "media": "http://media.com",
            "post_kateg": post_kateg1.pk,
            "title": "title",
        }

        at2 = date(year=2019, month=2, day=14)
        post_kateg2 = self.create_post_kateg("post_kateg2")
        data2 = {
            "at": at2,
            "content": "content1",
            "media": "http://mediaafs.com",
            "post_kateg": post_kateg2.pk,
            "title": "title1",
        }

        response = self.client.post(
            "/api/v1/post/", data=data1, content_type="application/json", **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            "/api/v1/post/",
            data=data2,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        at1 = date(year=2019, month=2, day=14)
        post_kateg1 = self.create_post_kateg("post_kateg1")
        ph1 = self.create_post(name="name1", at=at1, post_kateg=post_kateg1)

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "at": at1,
            "content": "content",
            "media": "http://media.com",
            "post_kateg": post_kateg1.pk,
            "title": "title",
        }

        response = self.client.put(
            f"/api/v1/post/{ph1.pk}/",
            data=data,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post/{ph1.pk}/",
            content_type="application/json",
            data=data,
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/post/{ph1.pk}/",
            data=data,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post/{ph1.pk}/",
            data=data,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self._delete_as(self.user_token)
        self._delete_as(self.admin_token)

    def _delete_as(self, token: Optional[str] = None):
        at1 = date(year=2019, month=2, day=14)
        post_kateg1 = self.create_post_kateg("post_kateg1")
        ph1 = self.create_post(name="name1", at=at1, post_kateg=post_kateg1)
        url = f"/api/v1/post/{ph1.pk}/"

        headers = {}
        if token:
            headers["HTTP_AUTHORIZATION"] = token

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
