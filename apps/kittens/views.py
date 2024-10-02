from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import KittenFilter
from .models import Kitten, Breed, Rating
from .serializers import (
    KittenDetailSerializer,
    KittenListSerializer,
    BreedSerializer,
    KittenSerializer,
    RatingSerializer,
)
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class KittenViewSet(viewsets.ModelViewSet):
    queryset = (
        Kitten.objects.select_related("breed", "added_by")
        .prefetch_related("ratings")
        .all()
    )
    serializer_class = KittenListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = KittenFilter
    filter_fields = ["breed"]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return KittenDetailSerializer
        elif self.action == "list":
            return KittenListSerializer
        return KittenSerializer


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.select_related("kitten", "user")
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
