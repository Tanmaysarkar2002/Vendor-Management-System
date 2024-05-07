from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import ExpressionWrapper, F, Avg, fields
from vendors.models import Vendor

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
(       'PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('COMPLETED', 'Completed'),
    ]
    
    po_number = models.CharField(max_length=50, unique=True ,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

        # Update the vendor's performance metrics.
        vendor = self.vendor
        po_queryset = PurchaseOrder.objects.filter(vendor=vendor)

        # On-Time Delivery Rate
        on_time_delivery_count = po_queryset.filter(status='completed', delivery_date__gte=self.delivery_date).count()
        completed_count = po_queryset.filter(status='completed').count()
        vendor.on_time_delivery_rate = (on_time_delivery_count / completed_count) * 100 if completed_count else 0

        # Quality Rating Average
        vendor.quality_rating = po_queryset.filter(status='completed').aggregate(average_quality=Coalesce(Avg('quality_rating'), 0.0))['average_quality']

        # Average Response Time
        response_time=ExpressionWrapper(F('acknowledgment_date') - F('order_date'), output_field=fields.FloatField())
        vendor.response_time = response_time

        # Fulfilment Rate
        fulfilled_count = po_queryset.filter(status='completed', acknowledgment_date__isnull=False).count()
        total_count = po_queryset.count()
        vendor.fulfillment_rate = (fulfilled_count / total_count) * 100 if total_count else 0

        vendor.save()

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"
    


