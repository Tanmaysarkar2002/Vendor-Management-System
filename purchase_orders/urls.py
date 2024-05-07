from django.urls import path
from .views import PurchaseOrderView

urlpatterns = [
    path('api/purchase-orders/', PurchaseOrderView.as_view(), name='Vendor'),
    path('api/purchase-orders/<int:purchase_id>/', PurchaseOrderView.as_view(), name='Vendor'),
]