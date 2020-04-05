from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.api.impl.v1.views import DiscountViewSet
from apps.api.impl.v1.views import KatalogViewSet
from apps.api.impl.v1.views import Post_kategViewSet
from apps.api.impl.v1.views import PostViewSet
from apps.api.impl.v1.views import TelegramView

router = DefaultRouter()
router.register("discount", DiscountViewSet)
router.register("katalog", KatalogViewSet)
router.register("post", PostViewSet)
router.register("post_kateg", Post_kategViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("telegram/", TelegramView.as_view()),
]
