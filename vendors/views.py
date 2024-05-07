from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Vendor
from .serializers import VendorSerializer ,VendorPerformanceSerializer

class VendorView(APIView):
    
    permission_classes = [IsAuthenticated]
                          
    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        if pk:
            vendor = self.get_object(pk)
        else:
            vendor = Vendor.objects.all()

        serializer = VendorSerializer(vendor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):

        data = request.data.copy()  
        data['vendor_code'] = get_random_string(length=32) 
        serializer = VendorSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, vendor_id):


        vendor = self.get_object(vendor_id)

        if not vendor:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializer(vendor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        if not vendor:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response({'Msg': 'Vendor Deleted'} , status=status.HTTP_204_NO_CONTENT)




class VendorPerformanceView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer