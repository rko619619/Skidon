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

        for obj, katalog in zip(payload, (katalog1,katalog2)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj,
                {"id": katalog.pk,
                 "title": katalog.title,
                 "content": katalog.content,
                 "media": katalog.media,
                 "adress": katalog.adress},
            )

    def test_retrieve(self):
        media = self.create_katalog("media")

        response = self.client.get(f"/api/v1/katalog/{media.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload, {"id": media.pk,
                      "title": media.title,
                      "content": media.content,
                      "media": media.media,
                      "adress": media.adress,
                      }
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content":"content" ,
            "media": "media",
            "adress":"adress",
                }

        response = self.client.post("/api/v1/katalog/", data=data,content_type="application/json", **user_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/api/v1/katalog/", data=data,content_type="application/json", **admin_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        media = self.create_discount("media")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content": "content",
            "media": "media",
            "adress": "adress",
        }

        response = self.client.put(
            f"/api/v1/katalog/{media.pk}/", data=data,content_type="application/json", **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/katalog/{media.pk}/", data=data,content_type="application/json", **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/katalog/{media.pk}/", data=data,content_type="application/json", **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/katalog/{media.pk}/", data=data,content_type="application/json", **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        media = self.create_discount("media")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "title": "title",
            "content": "content",
            "media": "media",
            "adress": "adress",
        }

        response = self.client.delete(
            f"/api/v1/katalog/{media.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(
            f"/api/v1/katalog/{media.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
