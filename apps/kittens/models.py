from django.db import models
from django.contrib.auth import get_user_model


class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Kitten(models.Model):
    COLOR_CHOICES = [
        ("black", "Black"),
        ("white", "White"),
        ("brown", "Brown"),
        ("grey", "Grey"),
        ("mixed", "Mixed"),
    ]

    name = models.CharField(max_length=100)
    breed = models.ForeignKey("Breed", on_delete=models.CASCADE, related_name="kittens")
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    age = models.PositiveIntegerField()
    description = models.TextField()
    added_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="kittens"
    )

    def __str__(self):
        return f"{self.name} ({self.breed.name})"


class Rating(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ("kitten", "user")
