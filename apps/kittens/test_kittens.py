import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.kittens.models import Kitten, Breed, Rating


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    user = User.objects.create_user(username="testuser", password="testpass")
    return user


@pytest.fixture
def breed(db):
    return Breed.objects.create(name="Siamese")


@pytest.fixture
def kitten(db, user, breed):
    return Kitten.objects.create(
        name="Fluffy",
        breed=breed,
        color="White",
        age=3,
        description="Cute kitten",
        added_by=user,
    )


# CREATE KITTENS
@pytest.mark.django_db
def test_create_kitten(api_client, breed, user):
    api_client.force_authenticate(user=user)

    data = {
        "name": "Fluffy",
        "breed_id": breed.id,
        "color": "white",
        "age": 2,
        "description": "A fluffy kitten",
    }

    response = api_client.post("/kittens/", data, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert Kitten.objects.count() == 1
    assert Kitten.objects.get().name == "Fluffy"

# GET KITTENS
@pytest.mark.django_db
def test_list_kittens(api_client, kitten):
    response = api_client.get("/kittens/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

# GET KITTEN
@pytest.mark.django_db
def test_retrieve_kitten(api_client, kitten):
    response = api_client.get(f"/kittens/{kitten.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == kitten.name

# UPDATE KITTEN
@pytest.mark.django_db
def test_update_kitten(api_client, kitten, user, breed):
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/kittens/{kitten.id}/",
        {
            "name": "Updated Fluffy",
            "breed": breed.id,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    kitten.refresh_from_db()
    assert kitten.name == "Updated Fluffy"

# DELETE KITTEN
@pytest.mark.django_db
def test_delete_kitten(api_client, kitten, user):
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"/kittens/{kitten.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Kitten.objects.count() == 0


@pytest.mark.django_db
def test_list_breeds(api_client, breed):
    response = api_client.get("/breeds/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_rating(api_client, user, kitten):
    api_client.force_authenticate(user=user)
    response = api_client.post("/ratings/", {"kitten": kitten.id, "score": 5})
    assert response.status_code == status.HTTP_201_CREATED
    assert Rating.objects.count() == 1


@pytest.mark.django_db
def test_list_ratings(api_client, user, kitten):
    Rating.objects.create(kitten=kitten, user=user, score=4)
    response = api_client.get("/ratings/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_rating(api_client, user, kitten):
    rating = Rating.objects.create(kitten=kitten, user=user, score=5)
    response = api_client.get(f"/ratings/{rating.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["score"] == rating.score


@pytest.mark.django_db
def test_update_rating(api_client, user, kitten):
    rating = Rating.objects.create(kitten=kitten, user=user, score=4)
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/ratings/{rating.id}/", {"score": 5})
    assert response.status_code == status.HTTP_200_OK
    rating.refresh_from_db()
    assert rating.score == 5


@pytest.mark.django_db
def test_delete_rating(api_client, user, kitten):
    rating = Rating.objects.create(kitten=kitten, user=user, score=4)
    api_client.force_authenticate(user=user)
    response = api_client.delete(f"/ratings/{rating.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Rating.objects.count() == 0
