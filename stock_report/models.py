from django.db import models

class StockReport(models.Model):
    client_id = models.CharField(max_length=50, db_index=True)

    product_code = models.CharField(max_length=30)
    product_name = models.CharField(max_length=200)
    productcode = models.CharField(max_length=30)
    barcode = models.CharField(max_length=35, null=True, blank=True)
    bmrp = models.DecimalField(max_digits=15, decimal_places=5, null=True)
    salesprice = models.DecimalField(max_digits=15, decimal_places=5, null=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=5, null=True)

    class Meta:
        db_table = "stock_report"
