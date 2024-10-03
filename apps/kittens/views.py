from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
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
        elif self.action == "rate_kitten":
            return RatingSerializer
        return KittenSerializer

    @action(detail=False, methods=["get"], url_path="breeds", url_name="breeds")
    def list_breeds(self, request):
        queryset = Breed.objects.all()
        serializer = BreedSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="rate",
        url_name="rate",
        permission_classes=[IsAuthenticated],
    )
    def rate_kitten(self, request, pk=None):
        kitten = self.get_object()
        user = request.user

        try:
            rating = Rating.objects.get(kitten=kitten, user=user)
            if rating.score == request.data.get("score"):
                return Response(
                    {
                        "detail": "You have already rated this kitten with the same score."
                    },
                    status=status.HTTP_200_OK,
                )
            serializer = RatingSerializer(rating, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=user, kitten=kitten)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rating.DoesNotExist:
            serializer = RatingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user, kitten=kitten)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
