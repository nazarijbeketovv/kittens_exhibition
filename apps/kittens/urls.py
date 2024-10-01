from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KittenViewSet, BreedViewSet, RatingViewSet

router = DefaultRouter()
router.register(r"kittens", KittenViewSet)
router.register(r"breeds", BreedViewSet)
router.register(r"ratings", RatingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
