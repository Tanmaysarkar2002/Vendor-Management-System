from django.urls import path
from .views import VendorView ,VendorPerformanceView

urlpatterns = [
    path('api/vendors/', VendorView.as_view(), name='Vendor'),
    path('api/vendors/<int:vendor_id>/', VendorView.as_view(), name='Vendor'),
    path('api/vendors/<int:pk>/performance', VendorPerformanceView.as_view(), name='vendor-performance'),
]