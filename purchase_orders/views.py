from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer ,GetPurchaseOrderSerializer



class PurchaseOrderView(APIView):
    
    permission_classes = [IsAuthenticated]
                          
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            return None

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        print(kwargs)
        if pk:
            purchase_order = self.get_object(pk)
        else:
            purchase_order = PurchaseOrder.objects.all()

        serializer = GetPurchaseOrderSerializer(purchase_order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):

        data = request.data.copy()  
        data['po_number'] = get_random_string(length=10) 

        print(data)
        serializer = PurchaseOrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, purchase_id):

        purchase_order = self.get_object(purchase_id)
        print(request.data)
        if not purchase_order:
            return Response({'error': 'PurchaseOrder not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, purchase_id):
        purchase_order = self.get_object(purchase_id)
        if not purchase_order:
            return Response({'error': 'PurchaseOrder not found'}, status=status.HTTP_404_NOT_FOUND)
        purchase_order.delete()
        return Response({'Msg': 'PurchaseOrder Deleted'},status=status.HTTP_204_NO_CONTENT)

