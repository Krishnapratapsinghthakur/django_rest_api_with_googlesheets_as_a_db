from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet
from .sheets_views import SheetItemListCreateAPIView, SheetItemDetailAPIView

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('sheet-items/', SheetItemListCreateAPIView.as_view(), name='sheet-item-list'),
    path('sheet-items/<int:row_id>/', SheetItemDetailAPIView.as_view(), name='sheet-item-detail'),
]