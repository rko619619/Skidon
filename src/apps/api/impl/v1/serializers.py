from rest_framework import serializers

from apps.about.models import Discount, Katalog,Post_kateg,Post

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
