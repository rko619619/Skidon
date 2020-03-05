from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from apps.about.models import Discount,Katalog,Post_kateg,Post

from apps.api.impl.v1.serializers import (
    DiscountSerializer,
    KatalogSerializer,
    Post_kategSerializer,
    PostSerializer,
)


class DiscountViewSet(ReadOnlyModelViewSet):
    querset= Discount.objects.all()
    serializer_class = DiscountSerializer

class KatalogViewSet(ReadOnlyModelViewSet):
    queryset = Katalog.objects.all()
    serializer_class = KatalogSerializer

class Post_kategViewSet(ReadOnlyModelViewSet):
    queryset = Post_kateg.objects.all()
    serializer_class = Post_kategSerializer

class PostViewSet(ListModelMixin, RetrieveModelMixin,CreateModelMixin, GenericViewSet):
    serializer_class = PostSerializer
    lookup_field = "post_kateg"
    queryset = Post.objects.all()