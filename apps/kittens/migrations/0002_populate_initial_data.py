from django.db import migrations
from django.contrib.auth import get_user_model
import random


def create_initial_data(apps, schema_editor):

    User = apps.get_model("auth", "User")
    Breed = apps.get_model("kittens", "Breed")
    Kitten = apps.get_model("kittens", "Kitten")
    Rating = apps.get_model("kittens", "Rating")

    breeds = [
        "Siamese",
        "Persian",
        "Siberian",
        "British Shorthair",
        "Maine Coon",
        "Scottish Fold",
    ]
    breed_objects = [Breed.objects.create(name=breed) for breed in breeds]

    users = []
    for i in range(50):
        user = User.objects.create_user(
            username=f"user_{i}", email=f"user_{i}@example.com", password="password123"
        )
        users.append(user)

    colors = ["black", "white", "brown", "grey", "mixed"]
    kittens = []
    for i in range(100):
        kitten = Kitten.objects.create(
            name=f"Kitten_{i}",
            breed=random.choice(breed_objects),
            color=random.choice(colors),
            age=random.randint(1, 10),
            description="A lovely kitten",
            added_by=random.choice(users),
        )
        kittens.append(kitten)

    for kitten in kittens:
        for user in random.sample(users, random.randint(1, 10)):
            Rating.objects.create(kitten=kitten, user=user, score=random.randint(1, 5))


class Migration(migrations.Migration):

    dependencies = [
        ("kittens", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
