from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()  # ✅ gallery images

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'description',
            'price',
            'image',     # main image
            'images',    # gallery images
        ]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_images(self, obj):
        # obj.gallery comes from related_name="gallery"
        return [img.image.url for img in obj.gallery.all()]
