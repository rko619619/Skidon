from typing import Optional

from rest_framework import status

from apps.api.tests.base import ApiTest


class DiscountApiTest(ApiTest):
    def test_read(self):
        discount1 = self.create_discount("discount1")
        discount2 = self.create_discount("discount2")

        headers = {"HTTP_AUTHORIZATION": self.admin_token}
        response = self.client.get("/api/v1/discount/", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, ph in zip(payload, (discount1, discount2)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(
                obj,
                {
                    "id": ph.pk,
                    "shop": ph.shop,
                    "name_of_discount": ph.name_of_discount,
                    "text": ph.text,
                    "price": ph.price,
                    "additional_media": ph.additional_media,
                    "media": ph.media,
                },
            )

    def test_retrieve(self):
        ph = self.create_discount("media")

        response = self.client.get(f"/api/v1/discount/{ph.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(
            payload,
            {
                "id": ph.pk,
                "shop": ph.shop,
                "name_of_discount": ph.name_of_discount,
                "text": ph.text,
                "price": ph.price,
                "additional_media": ph.additional_media,
                "media": ph.media,
            },
        )

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data1 = {
            "media": "http://test.test/test1",
            "shop": "shop1",
            "name_of_discount": "name1",
            "text": "text1",
            "price": "price",
            "additional_media": "http://test.test/test1",
        }
        data2 = {
            "media": "http://test.test/test1",
            "shop": "shop1",
            "name_of_discount": "name2",
            "text": "text2",
            "price": "price",
            "additional_media": "http://test.test/test1",
        }
        response = self.client.post(
            "/api/v1/discount/",
            data=data1,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        response = self.client.post(
            "/api/v1/discount/",
            data=data2,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        response = self.client.post(
            "/api/v1/discount/",
            data=data2,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.json()
        )

    def test_update(self):
        ph1 = self.create_discount("name1")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {
            "shop": "shop",
            "name_of_discount": "sad",
            "text": "sad",
            "price": "sdsa",
            "additional_media": "http://media.com",
            "media": "http://media.com",
        }

        response = self.client.put(
            f"/api/v1/discount/{ph1.pk}/",
            data=data,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/discount/{ph1.pk}/",
            data=data,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/discount/{ph1.pk}/",
            data=data,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/discount/{ph1.pk}/",
            data=data,
            content_type="application/json",
            **admin_headers,
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
