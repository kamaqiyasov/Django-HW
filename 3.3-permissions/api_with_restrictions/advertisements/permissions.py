from rest_framework.permissions import BasePermission, SAFE_METHODS

from advertisements.models import AdvertisementStatusChoices

class IsOwnerOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.creator