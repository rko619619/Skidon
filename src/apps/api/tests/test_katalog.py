from typing import Optional

from rest_framework import status

from apps.api.tests.base import ApiTest


class KatalogTest(ApiTest):
    def test_read(self):
        katalog1 = self.create_katalog("title")
        katalog2 = self.create_katalog("media")
        response = self.client.get("/api/v1/katalog/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, katalog in zip(payload, (katalog1, katalog2)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj,
                {
                    "id": katalog.pk,
                    "title": katalog.title,
                    "content": katalog.content,
                    "media": katalog.media,
                    "adress": katalog.adress,
                },
            )

    def test_retrieve(self):
        media = self.create_katalog("media")

        response = self.client.get(f"/api/v1/katalog/{media.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload,
            {
                "id": media.pk,
                "title": media.title,
                "content": media.content,
                "media": media.media,
                "adress": media.adress,
            },
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data1 = {
            "title": "title",
            "content": "content",
            "media": "http://test.test/test1",
            "adress": "adress",
        }
        data2 = {
            "title": "title1",
            "content": "content1",
            "media": "http://test.test/test11",
            "adress": "adress1",
        }

        response = self.client.post(
            "/api/v1/katalog/",
            data=data1,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            "/api/v1/katalog/",
            data=data2,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        ph1 = self.create_katalog("ph1")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data1 = {
            "title": "title",
            "content": "content",
            "media": "http://test.test/test1",
            "adress": "adress",
        }

        response = self.client.put(
            f"/api/v1/katalog/{ph1.pk}/",
            data=data1,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/katalog/{ph1.pk}/",
            data=data1,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/katalog/{ph1.pk}/",
            data=data1,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/katalog/{ph1.pk}/",
            data=data1,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self._delete_as(self.user_token)
        self._delete_as(self.admin_token)

    def _delete_as(self, token: Optional[str] = None):
        title = self.create_katalog("title")
        url = f"/api/v1/katalog/{title.pk}/"

        headers = {}
        if token:
            headers["HTTP_AUTHORIZATION"] = token

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
