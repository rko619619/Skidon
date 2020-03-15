from typing import Optional

from rest_framework import status

from apps.api.tests.base import ApiTest


class DiscountApiTest(ApiTest):
    def test_read(self):
        media = self.create_discount("media")
        shops = self.create_discount("shops")

        response = self.client.get("/api/v1/discount/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, discount in zip(payload, (media, shops)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj, {"id": discount.pk, "media": discount.media, "shop": discount.shop}
            )

    def test_retrieve(self):
        media = self.create_discount("media")

        response = self.client.get(f"/api/v1/discount/{media.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload, {"id": media.pk, "media": media.media, "shop": media.shop}
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data1 = {"media": "http://test.test/test1", "shop": "shop1"}

        response = self.client.post("/api/v1/discount/", data=data1, content_type="application/json", **user_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post("/api/v1/discount/", data=data1, content_type="application/json", **admin_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        ph1 = self.create_discount("name1")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"media": "http://name.com", "shop": "name"}

        response = self.client.put(
            f"/api/v1/discount/{ph1.pk}/", data=data, content_type="application/json", **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/discount/{ph1.pk}/", data=data, content_type="application/json", **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/discount/{ph1.pk}/", data=data, content_type="application/json", **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/discount/{ph1.pk}/", data=data, content_type="application/json", **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self._delete_as(self.user_token)
        self._delete_as(self.admin_token)

    def _delete_as(self, token: Optional[str] = None):
        media = self.create_discount("media")
        url = f"/api/v1/discount/{media.pk}/"

        headers = {}
        if token:
            headers["HTTP_AUTHORIZATION"] = token

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
