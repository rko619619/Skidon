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
        data1 = {"xxx": "abc"}
        data2 = {"xxxx": "abcd"}

        response = self.client.post("/api/v1/discount/", data=data1, **user_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post("/api/v1/discount/", data=data2, **admin_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        media = self.create_discount("media")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"media": "media", "shop": "shop"}

        response = self.client.put(
            f"/api/v1/discount/{media.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/discount/{media.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/discount/{media.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/discount/{media.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        media = self.create_discount("media")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"media": "media", "shop": "shop"}

        response = self.client.delete(
            f"/api/v1/discount/{media.pk}/", data=data, **user_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(
            f"/api/v1/discount/{media.pk}/", data=data, **admin_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
