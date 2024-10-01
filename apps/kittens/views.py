from rest_framework import viewsets, permissions
from .models import Kitten, Breed, Rating
from .serializers import KittenSerializer, BreedSerializer, RatingSerializer
from .permissions import IsOwnerOrReadOnly


class KittenViewSet(viewsets.ModelViewSet):
    queryset = (
        Kitten.objects.select_related("breed", "added_by")
        .prefetch_related("ratings")
        .all()
    )
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
