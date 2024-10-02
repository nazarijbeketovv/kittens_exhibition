from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

    @action(detail=False, methods=["get"], url_path="breeds", url_name="breeds")
    def list_breeds(self, request):
        queryset = Breed.objects.all()
        serializer = BreedSerializer(queryset, many=True)
        return Response(serializer.data)

    # TODO: to finish the func below
    @action(detail=True, methods=["post"], url_path="rate", url_name="rate")
    def set_rating(self, request, pk=None):
        kitten = self.get_object()
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(kitten=kitten, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
