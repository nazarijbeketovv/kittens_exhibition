from rest_framework import serializers
from .models import Kitten, Breed, Rating


from rest_framework import serializers
from .models import Kitten, Breed


class KittenSerializer(serializers.ModelSerializer):
    breed = serializers.CharField(source="breed.name", read_only=True)
    breed_id = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), source="breed", write_only=True
    )
    added_by = serializers.CharField(source="added_by.username", read_only=True)

    class Meta:
        model = Kitten
        fields = [
            "id",
            "name",
            "breed",
            "breed_id",
            "color",
            "age",
            "description",
            "added_by",
        ]
        read_only_fields = ["added_by", "breed"]

    def update(self, instance, validated_data):

        instance.name = validated_data.get("name", instance.name)
        instance.color = validated_data.get("color", instance.color)
        instance.age = validated_data.get("age", instance.age)
        instance.description = validated_data.get("description", instance.description)

        if "breed" in validated_data:
            instance.breed = validated_data["breed"]

        instance.save()
        return instance


class KittenListSerializer(serializers.ModelSerializer):
    breed = serializers.CharField(source="breed.name")
    added_by = serializers.CharField(source="added_by.username")

    class Meta:
        model = Kitten
        fields = ["id", "name", "breed", "added_by"]
        read_only_fields = ["added_by"]


class KittenDetailSerializer(serializers.ModelSerializer):
    breed = serializers.CharField(source="breed.name")
    added_by = serializers.CharField(source="added_by.username")

    class Meta:
        model = Kitten
        fields = ["id", "name", "breed", "color", "age", "description", "added_by"]
        read_only_fields = ["added_by"]


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ["name"]


class RatingSerializer(serializers.ModelSerializer):
    kitten = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Rating
        fields = ["kitten", "score"]
        read_only_fields = ["user"]
