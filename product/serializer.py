from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product


class ProductSerializer(ModelSerializer):

    def validate(self, data):
        context_data = self.context
        print("Serializer Context:", context_data)

        # Your validation logic
        if self.instance.pk is None:
            raise serializers.ValidationError("pk is required")

        # Don't forget to return the validated data
        return data

    class Meta:
        model = Product
        fields = "__all__"
