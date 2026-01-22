from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import StockReport


@api_view(["POST"])
def upload_stock_report(request):
    try:
        client_id = request.GET.get("client_id")

        if not client_id:
            return Response({"error": "client_id is required"}, status=400)

        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Expected list"}, status=400)

        with transaction.atomic():
            # Clear only this client's data
            StockReport.objects.filter(client_id=client_id).delete()

            objs = [
                StockReport(
                    client_id=client_id,
                    product_code=i.get("product_code"),
                    product_name=i.get("product_name"),
                    productcode=i.get("productcode"),
                    barcode=i.get("barcode"),
                    bmrp=i.get("bmrp"),
                    salesprice=i.get("salesprice"),
                    quantity=i.get("quantity"),
                )
                for i in data
            ]

            StockReport.objects.bulk_create(objs, batch_size=1000)

        return Response({
            "status": "success",
            "client_id": client_id,
            "records": len(objs)
        })

    except Exception as e:
        # THIS WILL SHOW THE REAL PROBLEM
        return Response({
            "status": "failed",
            "error": str(e)
        }, status=500)


@api_view(["GET"])
def get_stock_report(request):
    client_id = request.GET.get("client_id")

    if not client_id:
        return Response({"error": "client_id is required"}, status=400)

    qs = StockReport.objects.filter(client_id=client_id)
    return Response(list(qs.values()))
