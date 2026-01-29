from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Item model with user-specific data isolation.
    
    - Superusers can view all records
    - Regular users can only view their own records
    - User is auto-assigned on create
    """
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset based on user role:
        - Superusers see all records
        - Regular users see only their own records
        """
        user = self.request.user
        if user.is_superuser:
            return Item.objects.all()
        return Item.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Auto-assign the current logged-in user when creating a new record.
        """
        serializer.save(user=self.request.user)