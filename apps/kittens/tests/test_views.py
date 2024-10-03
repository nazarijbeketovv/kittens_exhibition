import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.kittens.models import Kitten, Breed, Rating
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_breed(db):
    return Breed.objects.create(name="Siamese")


@pytest.fixture
def create_kitten(db, create_breed, create_user):
    user = create_user(username="testuser", password="testpass")
    return Kitten.objects.create(
        name="Fluffy",
        breed=create_breed,
        color="white",
        age=1,
        description="Very cute kitten",
        added_by=user,
    )


### 1.1. Тест создания котенка
@pytest.mark.django_db
def test_create_kitten(api_client, create_breed, create_user):
    user = create_user(username="testuser", password="testpass")
    api_client.force_authenticate(user=user)
    url = reverse("kitten-list")
    data = {
        "name": "Fluffy",
        "breed_id": create_breed.id,
        "color": "white",
        "age": 2,
        "description": "A very cute kitten",
    }
    amount_of_kittens = Kitten.objects.count()

    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Kitten.objects.count() == amount_of_kittens + 1

    assert Kitten.objects.order_by("-id").first().name == "Fluffy"


### 1.2. Тест получения списка котят
@pytest.mark.django_db
def test_list_kittens(api_client, create_kitten):
    url = reverse("kitten-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[-1]["name"] == create_kitten.name


### 1.3. Тест оценки котенка
@pytest.mark.django_db
def test_create_kitten_rating(api_client, create_kitten, create_user):
    """Тестируем создание нового рейтинга для котенка"""
    user = create_user(username="rating_user", password="ratingpass")
    api_client.force_authenticate(user=user)
    url = reverse("kitten-rate", args=[create_kitten.id])
    data = {"score": 4}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Rating.objects.filter(kitten=create_kitten, user=user).exists()
    assert Rating.objects.get(kitten=create_kitten, user=user).score == 4


@pytest.mark.django_db
def test_update_kitten_rating(api_client, create_kitten, create_user):
    """Тестируем обновление рейтинга для котенка"""
    user = create_user(username="rating_user", password="ratingpass")
    api_client.force_authenticate(user=user)
    url = reverse("kitten-rate", args=[create_kitten.id])

    # Сначала создаем рейтинг
    api_client.post(url, {"score": 4}, format="json")

    # Обновляем рейтинг
    response = api_client.post(url, {"score": 5}, format="json")

    assert response.status_code == status.HTTP_200_OK
    rating = Rating.objects.get(kitten=create_kitten, user=user)
    assert rating.score == 5


@pytest.mark.django_db
def test_same_rating_twice(api_client, create_kitten, create_user):
    """Тестируем выставление того же рейтинга дважды"""
    user = create_user(username="rating_user", password="ratingpass")
    api_client.force_authenticate(user=user)
    url = reverse("kitten-rate", args=[create_kitten.id])

    # Создаем рейтинг
    api_client.post(url, {"score": 4}, format="json")

    # Пытаемся установить тот же рейтинг
    response = api_client.post(url, {"score": 4}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.data["detail"]
        == "You have already rated this kitten with the same score."
    )
