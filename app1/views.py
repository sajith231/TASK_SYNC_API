from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AccUsers, Misel, AccMaster, AccLedgers, AccInvmast, CashAndBankAccMaster, AccTtServicemaster, SalesDaywise, SalesMonthwise,SalesToday, PurchaseToday
from .models import SalesReturnReport
import traceback
import logging

logger = logging.getLogger(__name__)


class UploadAccUsersAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of user items."}, status=400)

        try:
            AccUsers.objects.filter(client_id=client_id).delete()

            for item in data:
                AccUsers.objects.create(
                    id=item['id'],
                    pass_field=item['pass'],
                    role=item.get('role'),
                    accountcode=item.get('accountcode'),
                    client_id=client_id
                )

            return Response({"message": f"{len(data)} users uploaded for client_id {client_id}."}, status=201)

        except Exception as e:
            logger.error(f"Error in UploadAccUsersAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetAccUsersAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        users = AccUsers.objects.filter(client_id=client_id)
        data = [{
            "id": u.id,
            "pass": u.pass_field,
            "role": u.role,
            "accountcode": u.accountcode,
        } for u in users]

        return Response({"count": len(data), "users": data}, status=200)


class UploadMiselAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of misel items."}, status=400)

        try:
            Misel.objects.filter(client_id=client_id).delete()

            for item in data:
                Misel.objects.create(
                    firm_name=item.get('firm_name'),
                    address=item.get('address'),
                    phones=item.get('phones'),
                    mobile=item.get('mobile'),
                    address1=item.get('address1'),
                    address2=item.get('address2'),
                    address3=item.get('address3'),
                    pagers=item.get('pagers'),
                    tinno=item.get('tinno'),
                    client_id=client_id
                )

            return Response({"message": f"{len(data)} misel records uploaded for client_id {client_id}."}, status=201)

        except Exception as e:
            logger.error(f"Error in UploadMiselAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetMiselAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        misel = Misel.objects.filter(client_id=client_id)
        data = [{
            "firm_name": m.firm_name,
            "address": m.address,
            "phones": m.phones,
            "mobile": m.mobile,
            "address1": m.address1,
            "address2": m.address2,
            "address3": m.address3,
            "pagers": m.pagers,
            "tinno": m.tinno
        } for m in misel]

        return Response({"count": len(data), "misel": data}, status=200)


class UploadAccMasterAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')
        append = request.query_params.get('append', 'false').lower() == 'true'

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of acc_master items."}, status=400)

        try:
            if not append:
                AccMaster.objects.filter(client_id=client_id).delete()

            for item in data:
                acc_master, created = AccMaster.objects.update_or_create(
                    code=item['code'],
                    client_id=client_id,
                    defaults={
                        'name': item.get('name'),
                        'super_code': item.get('super_code'),
                        'opening_balance': item.get('opening_balance'),
                        'debit': item.get('debit'),
                        'credit': item.get('credit'),
                        'place': item.get('place'),
                        'phone2': item.get('phone2'),
                        'openingdepartment': item.get('openingdepartment'),
                        'area': item.get('area') if item.get('area') else None,
                    }
                )

            action = "appended" if append else "uploaded (old data cleared)"
            return Response({"message": f"{len(data)} acc_master records {action} for client_id {client_id}."}, status=201)

        except Exception as e:
            logger.error(f"Error in UploadAccMasterAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetAccMasterAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        acc_master = AccMaster.objects.filter(client_id=client_id)
        data = [{
            "code": m.code,
            "name": m.name,
            "super_code": m.super_code if m.super_code else "",
            "opening_balance": str(m.opening_balance) if m.opening_balance is not None else None,
            "debit": str(m.debit) if m.debit is not None else None,
            "credit": str(m.credit) if m.credit is not None else None,
            "place": m.place,
            "phone2": m.phone2,
            "openingdepartment": m.openingdepartment,
            "area": m.area if m.area else ""
        } for m in acc_master]

        return Response({"count": len(data), "acc_master": data}, status=200)


class UploadAccLedgersAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')
        append = request.query_params.get('append', 'false').lower() == 'true'

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of acc_ledgers items."}, status=400)

        try:
            if not append:
                AccLedgers.objects.filter(client_id=client_id).delete()

            for item in data:
                AccLedgers.objects.create(
                    code=item['code'],
                    particulars=item.get('particulars'),
                    debit=item.get('debit'),
                    credit=item.get('credit'),
                    entry_mode=item.get('entry_mode'),
                    entry_date=item.get('entry_date'),
                    voucher_no=item.get('voucher_no'),
                    narration=item.get('narration'),
                    super_code=item.get('super_code'),
                    client_id=client_id
                )

            action = "appended" if append else "uploaded (old data cleared)"
            return Response({"message": f"{len(data)} acc_ledgers records {action} for client_id {client_id}."}, status=201)

        except Exception as e:
            logger.error(f"Error in UploadAccLedgersAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetAccLedgersAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        acc_ledgers = AccLedgers.objects.filter(client_id=client_id)
        data = [{
            "code": l.code,
            "particulars": l.particulars,
            "debit": str(l.debit) if l.debit else None,
            "credit": str(l.credit) if l.credit else None,
            "entry_mode": l.entry_mode,
            "entry_date": l.entry_date.strftime('%Y-%m-%d') if l.entry_date else None,
            "voucher_no": l.voucher_no,
            "narration": l.narration,
            "super_code": l.super_code if l.super_code else ""
        } for l in acc_ledgers]

        return Response({"count": len(data), "acc_ledgers": data}, status=200)


from datetime import datetime
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response

class UploadAccInvmastAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of acc_invmast items."}, status=400)

        try:
            # keep existing behaviour
            AccInvmast.objects.filter(client_id=client_id).delete()

            for item in data:
                invdate = item.get('invdate')
                if invdate:
                    try:
                        invdate = datetime.strptime(invdate, "%Y-%m-%d").date()
                    except Exception:
                        invdate = None

                AccInvmast.objects.create(
                    modeofpayment=item.get('modeofpayment'),
                    customerid=item.get('customerid'),
                    invdate=invdate,
                    nettotal=item.get('nettotal'),
                    paid=item.get('paid'),
                    bill_ref=item.get('bill_ref'),

                    # 🔹 NEW (unchanged behaviour)
                    userid=item.get('userid'),
                    type=item.get('type'),

                    client_id=client_id
                )

            return Response(
                {"message": f"{len(data)} acc_invmast records uploaded for client_id {client_id}."},
                status=201
            )

        except Exception as e:
            logger.error(f"Error in UploadAccInvmastAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetAccInvmastAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        acc_invmast = AccInvmast.objects.filter(client_id=client_id)

        data = [{
            "modeofpayment": i.modeofpayment,
            "customerid": i.customerid,
            "invdate": i.invdate.strftime('%Y-%m-%d') if i.invdate else None,
            "nettotal": str(i.nettotal) if i.nettotal else None,
            "paid": str(i.paid) if i.paid else None,
            "bill_ref": i.bill_ref,

            # 🔹 NEW (only returned, nothing else changed)
            "userid": i.userid,
            "type": i.type,

        } for i in acc_invmast]

        return Response(
            {"count": len(data), "acc_invmast": data},
            status=200
        )

class UploadCashAndBankAccMasterAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')
        force_clear = request.query_params.get('force_clear', 'false').lower() == 'true'

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of cashandbankaccmaster items."}, status=400)

        try:
            # Always clear existing data first to avoid duplicate key errors
            deleted_count = CashAndBankAccMaster.objects.filter(client_id=client_id).delete()[0]
            if deleted_count > 0:
                logger.info(f"Deleted {deleted_count} existing cashandbankaccmaster records for client {client_id}")
            
            # If empty list, just return success after clearing
            if len(data) == 0:
                return Response({"message": f"Cleared cashandbankaccmaster data for client_id {client_id}."}, status=200)

            # Insert new records
            for item in data:
                CashAndBankAccMaster.objects.create(
                    code=item['code'],
                    name=item['name'],
                    super_code=item.get('super_code'),
                    opening_balance=item.get('opening_balance'),
                    opening_date=item.get('opening_date'),
                    debit=item.get('debit'),
                    credit=item.get('credit'),
                    client_id=client_id
                )

            return Response({"message": f"{len(data)} cashandbankaccmaster records uploaded for client_id {client_id}."}, status=201)

        except Exception as e:
            logger.error(f"Error in UploadCashAndBankAccMasterAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetCashAndBankAccMasterAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        cashandbankaccmaster = CashAndBankAccMaster.objects.filter(client_id=client_id)
        data = [{
            "code": m.code,
            "name": m.name,
            "super_code": m.super_code,
            "opening_balance": str(m.opening_balance) if m.opening_balance else None,
            "opening_date": m.opening_date.strftime('%Y-%m-%d') if m.opening_date else None,
            "debit": str(m.debit) if m.debit else None,
            "credit": str(m.credit) if m.credit else None,
        } for m in cashandbankaccmaster]

        return Response({"count": len(data), "cashandbankaccmaster": data}, status=200)


class UploadAccTtServicemasterAPI(APIView):
    def post(self, request):
        """
        Upload acc_tt_servicemaster data with enhanced error handling
        """
        try:
            data = request.data
            client_id = request.query_params.get('client_id')
            
            # Validation
            if not client_id:
                logger.error("Missing client_id in request")
                return Response({"error": "Missing client_id"}, status=400)
            
            if not isinstance(data, list):
                logger.error(f"Expected list but got {type(data)}")
                return Response({"error": "Expected list"}, status=400)
            
            if len(data) == 0:
                logger.warning("Empty data array received")
                return Response({"message": "No data to upload"}, status=200)
            
            # Log first record for debugging
            logger.info(f"Received {len(data)} records. First record: {data[0] if data else 'None'}")
            
            # Delete existing records
            deleted_count = AccTtServicemaster.objects.filter(client_id=client_id).delete()[0]
            logger.info(f"Deleted {deleted_count} existing records for client {client_id}")
            
            # Insert new records
            created_count = 0
            for idx, row in enumerate(data):
                try:
                    # Validate required fields
                    if 'slno' not in row:
                        logger.error(f"Record {idx}: Missing 'slno' field. Data: {row}")
                        continue
                    
                    # Convert slno to integer if it's not already
                    slno_value = int(float(row['slno'])) if row['slno'] is not None else None
                    
                    if slno_value is None:
                        logger.error(f"Record {idx}: slno is None. Data: {row}")
                        continue
                    
                    AccTtServicemaster.objects.create(
                        slno=slno_value,
                        type=row.get('type'),
                        code=row.get('code'),
                        name=row.get('name'),
                        client_id=client_id
                    )
                    created_count += 1
                    
                except Exception as row_error:
                    logger.error(f"Error processing record {idx}: {str(row_error)}. Data: {row}")
                    logger.error(traceback.format_exc())
                    continue
            
            logger.info(f"Successfully created {created_count} records")
            return Response({
                "message": f"{created_count} acc_tt_servicemaster rows uploaded successfully",
                "created": created_count,
                "total_received": len(data)
            }, status=201)
            
        except Exception as e:
            error_msg = f"Critical error in UploadAccTtServicemasterAPI: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            return Response({"error": error_msg}, status=500)


class GetAccTtServicemasterAPI(APIView):
    def get(self, request):
        try:
            client_id = request.query_params.get('client_id')
            if not client_id:
                return Response({"error": "Missing client_id"}, status=400)

            rows = AccTtServicemaster.objects.filter(client_id=client_id)
            data = [{
                "slno": int(r.slno),
                "type": r.type,
                "code": r.code,
                "name": r.name
            } for r in rows]
            
            return Response({"count": len(data), "acc_tt_servicemaster": data}, status=200)
            
        except Exception as e:
            logger.error(f"Error in GetAccTtServicemasterAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)

# GET http://127.0.0.1:8000/api/get-users/?client_id=CLIENT001
# GET http://127.0.0.1:8000/api/get-misel/?client_id=CLIENT001
# GET http://127.0.0.1:8000/api/get-acc-master/?client_id=CLIENT001
# GET http://127.0.0.1:8000/api/get-acc-ledgers/?client_id=CLIENT001
# GET http://127.0.0.1:8000/api/get-acc-invmast/?client_id=CLIENT001



# NEW: Sales Today API Views
class UploadSalesTodayAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of sales_today items."}, status=400)

        try:
            # Clear existing data
            SalesToday.objects.filter(client_id=client_id).delete()

            # Insert new records
            for item in data:
                SalesToday.objects.create(
                    nettotal=item.get('nettotal'),
                    billno=item.get('billno'),
                    type=item.get('type'),
                    userid=item.get('userid'),
                    invdate=item.get('invdate'),
                    customername=item.get('customername'),
                    client_id=client_id
                )

            return Response({
                "message": f"{len(data)} sales_today records uploaded for client_id {client_id}."
            }, status=201)

        except Exception as e:
            logger.error(f"Error in UploadSalesTodayAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetSalesTodayAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        sales_today = SalesToday.objects.filter(client_id=client_id).order_by('-invdate', '-billno')
        data = [{
            "nettotal": str(s.nettotal) if s.nettotal else None,
            "billno": s.billno,
            "type": s.type,
            "userid": s.userid,
            "invdate": s.invdate.strftime('%Y-%m-%d') if s.invdate else None,
            "customername": s.customername
        } for s in sales_today]

        return Response({"count": len(data), "sales_today": data}, status=200)


# NEW: Purchase Today API Views
class UploadPurchaseTodayAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of purchase_today items."}, status=400)

        try:
            # Clear existing data
            PurchaseToday.objects.filter(client_id=client_id).delete()

            # Insert new records
            for item in data:
                PurchaseToday.objects.create(
                    net=item.get('net'),
                    billno=item.get('billno'),
                    pbillno=item.get('pbillno'),
                    date=item.get('date'),
                    total=item.get('total'),
                    suppliername=item.get('suppliername'),
                    client_id=client_id
                )

            return Response({
                "message": f"{len(data)} purchase_today records uploaded for client_id {client_id}."
            }, status=201)

        except Exception as e:
            logger.error(f"Error in UploadPurchaseTodayAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetPurchaseTodayAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        purchase_today = PurchaseToday.objects.filter(client_id=client_id).order_by('-date', '-billno')
        data = [{
            "net": str(p.net) if p.net else None,
            "billno": p.billno,
            "pbillno": p.pbillno,
            "date": p.date.strftime('%Y-%m-%d') if p.date else None,
            "total": str(p.total) if p.total else None,
            "suppliername": p.suppliername
        } for p in purchase_today]

        return Response({"count": len(data), "purchase_today": data}, status=200)
    




class UploadSalesDaywiseAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of sales_daywise items."}, status=400)

        try:
            # Clear existing data for this client
            SalesDaywise.objects.filter(client_id=client_id).delete()

            # Insert new records
            for item in data:
                SalesDaywise.objects.create(
                    date=item.get('date'),
                    total_bills=item.get('total_bills', 0),
                    total_amount=item.get('total_amount', 0),
                    client_id=client_id
                )

            return Response({
                "message": f"{len(data)} sales_daywise records uploaded for client_id {client_id}."
            }, status=201)

        except Exception as e:
            logger.error(f"Error in UploadSalesDaywiseAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetSalesDaywiseAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        sales_daywise = SalesDaywise.objects.filter(client_id=client_id).order_by('-date')
        data = [{
            "date": s.date.strftime('%Y-%m-%d') if s.date else None,
            "total_bills": s.total_bills,
            "total_amount": str(s.total_amount) if s.total_amount else "0.000"
        } for s in sales_daywise]

        return Response({"count": len(data), "sales_daywise": data}, status=200)


# NEW: Sales Monthwise API Views
class UploadSalesMonthwiseAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of sales_monthwise items."}, status=400)

        try:
            # Get current year to limit deletion scope
            from datetime import datetime
            current_year = datetime.now().year
            
            # Clear existing data for current year only
            SalesMonthwise.objects.filter(client_id=client_id, year=current_year).delete()

            # Insert new records
            for item in data:
                SalesMonthwise.objects.create(
                    month_name=item.get('month_name'),
                    month_number=item.get('month_number'),
                    year=item.get('year', current_year),
                    total_bills=item.get('total_bills', 0),
                    total_amount=item.get('total_amount', 0),
                    client_id=client_id
                )

            return Response({
                "message": f"{len(data)} sales_monthwise records uploaded for client_id {client_id}."
            }, status=201)

        except Exception as e:
            logger.error(f"Error in UploadSalesMonthwiseAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetSalesMonthwiseAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        sales_monthwise = SalesMonthwise.objects.filter(client_id=client_id).order_by('year', 'month_number')
        data = [{
            "month_name": s.month_name,
            "month_number": s.month_number,
            "year": s.year,
            "total_bills": s.total_bills,
            "total_amount": str(s.total_amount) if s.total_amount else "0.000"
        } for s in sales_monthwise]

        return Response({"count": len(data), "sales_monthwise": data}, status=200)
    





class UploadSalesReturnReportAPI(APIView):
    def post(self, request):
        data = request.data
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        if not isinstance(data, list):
            return Response({"error": "Expected a list of salesreturn_report items."}, status=400)

        try:
            # Clear existing data
            SalesReturnReport.objects.filter(client_id=client_id).delete()

            # Insert new records
            for item in data:
                SalesReturnReport.objects.create(
                    date=item.get('date'),
                    invno=item.get('invno'),
                    net=item.get('net'),
                    customername=item.get('customername'),
                    userid=item.get('userid'),
                    client_id=client_id
                )

            return Response({
                "message": f"{len(data)} salesreturn_report records uploaded for client_id {client_id}."
            }, status=201)

        except Exception as e:
            logger.error(f"Error in UploadSalesReturnReportAPI: {str(e)}\n{traceback.format_exc()}")
            return Response({"error": str(e)}, status=500)


class GetSalesReturnReportAPI(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "Missing client_id in query parameters."}, status=400)

        salesreturn_report = SalesReturnReport.objects.filter(client_id=client_id).order_by('-date', '-invno')
        data = [{
            "date": s.date.strftime('%Y-%m-%d') if s.date else None,
            "invno": s.invno,
            "net": str(s.net) if s.net else None,
            "customername": s.customername,
            "userid": s.userid
        } for s in salesreturn_report]

        return Response({"count": len(data), "salesreturn_report": data}, status=200)