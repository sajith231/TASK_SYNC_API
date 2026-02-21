from django.db import models

class AccUsers(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    pass_field = models.CharField(max_length=100, db_column='pass')
    role = models.CharField(max_length=30, blank=True, null=True)
    accountcode = models.CharField(max_length=30, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'acc_users'
        managed = True
        unique_together = ('id', 'client_id')


class Misel(models.Model):
    firm_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    phones = models.CharField(max_length=60, blank=True, null=True)
    mobile = models.CharField(max_length=60, blank=True, null=True)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    address3 = models.CharField(max_length=50, blank=True, null=True)
    pagers = models.CharField(max_length=60, blank=True, null=True)
    tinno = models.CharField(max_length=30, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'misel'
        managed = True


class AccMaster(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200, blank=True, null=True)
    super_code = models.CharField(max_length=5, blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    place = models.CharField(max_length=100, blank=True, null=True)
    phone2 = models.CharField(max_length=60, blank=True, null=True)
    openingdepartment = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=200, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'acc_master'
        managed = True
        unique_together = ('code', 'client_id')


class AccLedgers(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    particulars = models.CharField(max_length=500, blank=True, null=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    credit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    entry_mode = models.CharField(max_length=20, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    voucher_no = models.IntegerField(blank=True, null=True)
    narration = models.TextField(blank=True, null=True)
    super_code = models.CharField(max_length=5, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'acc_ledgers'
        managed = True


class AccInvmast(models.Model):
    id = models.AutoField(primary_key=True)
    slno = models.BigIntegerField(blank=True, null=True)  # ✅ NEW
    modeofpayment = models.CharField(max_length=10, blank=True, null=True)
    customerid = models.CharField(max_length=30, blank=True, null=True)
    invdate = models.DateField(blank=True, null=True)
    nettotal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    paid = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    bill_ref = models.CharField(max_length=100, blank=True, null=True)

    userid = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'acc_invmast'
        managed = True


class CashAndBankAccMaster(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=250)
    super_code = models.CharField(max_length=5, blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    opening_date = models.DateField(blank=True, null=True)
    debit = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    credit = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'cashandbankaccmaster'
        managed = True
        unique_together = ('code', 'client_id')


class AccTtServicemaster(models.Model):
    # FIXED: Use AutoField for id and make slno a regular field with unique constraint per client
    id = models.AutoField(primary_key=True)
    slno = models.IntegerField()
    type = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'acc_tt_servicemaster'
        managed = True
        unique_together = ('slno', 'client_id')  # Ensures slno is unique per client






class SalesToday(models.Model):
    """Sales records from acc_invmast where billno > 0"""
    id = models.AutoField(primary_key=True)
    nettotal = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    billno = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    userid = models.CharField(max_length=10, blank=True, null=True)
    invdate = models.DateField(blank=True, null=True)
    customername = models.CharField(max_length=250, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'sales_today'
        managed = True
        indexes = [
            models.Index(fields=['client_id', 'invdate']),
            models.Index(fields=['billno']),
        ]


class PurchaseToday(models.Model):
    """Purchase records from acc_purchasemaster where billno > 0"""
    id = models.AutoField(primary_key=True)
    net = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    billno = models.IntegerField(blank=True, null=True)
    pbillno = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    suppliername = models.CharField(max_length=250, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'purchase_today'
        managed = True
        indexes = [
            models.Index(fields=['client_id', 'date']),
            models.Index(fields=['billno']),
        ]






class PurchaseToday(models.Model):
    """Purchase records from acc_purchasemaster where billno > 0"""
    id = models.AutoField(primary_key=True)
    net = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    billno = models.IntegerField(blank=True, null=True)
    pbillno = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    suppliername = models.CharField(max_length=250, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'purchase_today'
        managed = True
        indexes = [
            models.Index(fields=['client_id', 'date']),
            models.Index(fields=['billno']),
        ]


class SalesDaywise(models.Model):
    """Sales summary by date for last 8 days"""
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    total_bills = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'sales_daywise'
        managed = True
        unique_together = ('date', 'client_id')
        indexes = [
            models.Index(fields=['client_id', 'date']),
        ]


class SalesMonthwise(models.Model):
    """Sales summary by month for current year"""
    id = models.AutoField(primary_key=True)
    month_name = models.CharField(max_length=20)  # e.g., "January 2025"
    month_number = models.IntegerField()  # 1-12
    year = models.IntegerField()
    total_bills = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'sales_monthwise'
        managed = True
        unique_together = ('month_number', 'year', 'client_id')
        indexes = [
            models.Index(fields=['client_id', 'year', 'month_number']),
        ]





class SalesReturnReport(models.Model):
    """Sales return records from acc_invoicereturn"""
    id = models.AutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    invno = models.IntegerField(blank=True, null=True)
    net = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    customername = models.CharField(max_length=250, blank=True, null=True)
    userid = models.CharField(max_length=13, blank=True, null=True)
    client_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'salesreturn_report'
        managed = True
        indexes = [
            models.Index(fields=['client_id', 'date']),
            models.Index(fields=['invno']),
        ]