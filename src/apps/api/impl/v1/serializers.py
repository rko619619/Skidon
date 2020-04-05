from rest_framework import serializers

from apps.about.models import Discount
from apps.about.models import Katalog
from apps.about.models import Post
from apps.about.models import Post_kateg


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"


class KatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Katalog
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class Post_kategSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_kateg
        fields = "__all__"
