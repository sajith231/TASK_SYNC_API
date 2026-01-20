from django.db import models


class AccSalesType(models.Model):
    cd = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "acc_sales_types"
