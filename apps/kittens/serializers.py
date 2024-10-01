from rest_framework import serializers
from .models import Kitten, Breed, Rating


class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ["id", "name", "breed", "color", "age", "description", "added_by"]
        read_only_fields = ["added_by"]


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ["id", "name"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["kitten", "user", "score"]
        read_only_fields = ["user"]
