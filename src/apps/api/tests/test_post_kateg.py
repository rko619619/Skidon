from typing import Optional

from rest_framework import status

from apps.api.tests.base import ApiTest


class Post_kategTest(ApiTest):
    def test_read(self):
        name1 = self.create_post_kateg("name1")
        name2 = self.create_post_kateg("name2")
        response = self.client.get("/api/v1/post_kateg/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertEqual(len(payload), 2)

        for obj, post_kateg in zip(payload, (name1, name2)):
            self.assertTrue(obj)
            self.assertIsInstance(obj, dict)

            self.assertDictEqual(obj, {"id": post_kateg.pk, "name": post_kateg.name})

    def test_retrieve(self):
        name = self.create_post_kateg("name")

        response = self.client.get(f"/api/v1/post_kateg/{name.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        self.assertIsInstance(payload, dict)

        self.assertDictEqual(payload, {"id": name.pk, "name": name.name})

    def test_create(self):
        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data1 = {"name": "name"}

        response = self.client.post(
            "/api/v1/post_kateg/",
            data=data1,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            "/api/v1/post_kateg/",
            data=data1,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        name = self.create_post_kateg("name")

        user_headers = {"HTTP_AUTHORIZATION": self.user_token}
        admin_headers = {"HTTP_AUTHORIZATION": self.admin_token}
        data = {"name": "name"}

        response = self.client.put(
            f"/api/v1/post_kateg/{name.pk}/",
            data=data,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post_kateg/{name.pk}/",
            data=data,
            content_type="application/json",
            **user_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            f"/api/v1/post_kateg/{name.pk}/",
            data=data,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            f"/api/v1/post_kateg/{name.pk}/",
            data=data,
            content_type="application/json",
            **admin_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self._delete_as(self.user_token)
        self._delete_as(self.admin_token)

    def _delete_as(self, token: Optional[str] = None):
        name = self.create_post_kateg("name")
        url = f"/api/v1/post_kateg/{name.pk}/"

        headers = {}
        if token:
            headers["HTTP_AUTHORIZATION"] = token

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
