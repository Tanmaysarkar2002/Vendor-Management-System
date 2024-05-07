from rest_framework import serializers
from .models import PurchaseOrder
from vendors.models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class GetPurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'