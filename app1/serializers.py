from rest_framework import serializers
from .models import AccUsers, Misel, AccLedgers, AccMaster, AccInvmast, CashAndBankAccMaster, AccTtServicemaster,SalesReturnReport


class AccUsersSerializer(serializers.ModelSerializer):
    pass_field = serializers.CharField(source='pass_field', max_length=100)

    class Meta:
        model = AccUsers
        fields = ['id', 'pass_field', 'role', 'accountcode', 'client_id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['pass'] = data.pop('pass_field')
        return data

    def to_internal_value(self, data):
        if 'pass' in data:
            data['pass_field'] = data.pop('pass')
        return super().to_internal_value(data)


class MiselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Misel
        fields = ['firm_name', 'address', 'phones', 'mobile',
                  'address1', 'address2', 'address3', 'pagers',
                  'tinno', 'client_id']


class AccMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccMaster
        fields = ['code', 'name', 'super_code', 'opening_balance', 'debit', 'credit',
                  'place', 'phone2', 'openingdepartment', 'area', 'client_id']


class AccLedgersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccLedgers
        fields = ['code', 'particulars', 'debit', 'credit', 'entry_mode',
                  'entry_date', 'voucher_no', 'narration', 'super_code', 'client_id']


class AccInvmastSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccInvmast
        fields = ['modeofpayment', 'customerid', 'invdate', 'nettotal',
                  'paid', 'bill_ref', 'userid', 'type', 'client_id']


class CashAndBankAccMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashAndBankAccMaster
        fields = ['code', 'name', 'super_code', 'opening_balance', 'opening_date', 
                  'debit', 'credit', 'client_id']


class AccTtServicemasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccTtServicemaster
        fields = ['slno', 'type', 'code', 'name', 'client_id']



class SalesReturnReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesReturnReport
        fields = ['date', 'invno', 'net', 'customername', 'userid', 'client_id']