from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KittenViewSet

router = DefaultRouter()
router.register(r"kittens", KittenViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
