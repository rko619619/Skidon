from django.urls import include, path
from rest_framework.routers import DefaultRouter


from apps.api.impl.v1.views import (
    DiscountViewSet,
    KatalogViewSet,
    PostViewSet,
    Post_kategViewSet,
)
from apps.api.impl.v1.views import TelegramView

router = DefaultRouter()
router.register('discount', DiscountViewSet)
router.register('katalog', KatalogViewSet)
router.register('post', PostViewSet)
router.register('post_kateg', Post_kategViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("telegram/", TelegramView.as_view()),
]