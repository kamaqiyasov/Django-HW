from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_queryset(self):
        queryset = Advertisement.objects.filter(status__in=['OPEN', 'CLOSED'])
        if self.request.user.is_authenticated:
            return queryset | Advertisement.objects.filter(creator=self.request.user)
        return queryset
    
    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        if self.action == 'favorite':
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        advertisement = self.get_object()
        user = request.user
        if request.method == 'POST':
            if advertisement.creator == user:
                return Response({'error': 'Нельзя добавить своё объявление'}, 
                            status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.get_or_create(creator=user, advertisement=advertisement)
            return Response({'status': 'Добавлено в избранное'})
        elif request.method == 'DELETE':
            Favorite.objects.filter(creator=user, advertisement=advertisement).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)