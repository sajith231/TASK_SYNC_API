import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StockReport


@csrf_exempt
def upload_stock_report(request):
    data = json.loads(request.body or "[]")

    StockReport.objects.all().delete()

    objs = [
        StockReport(
            code=row.get("code"),
            name=row.get("name"),
            productcode=row.get("productcode"),
            barcode=row.get("barcode"),
            bmrp=row.get("bmrp"),
            salesprice=row.get("salesprice"),
            quantity=row.get("quantity"),
        )
        for row in data
        if row.get("productcode")
    ]

    StockReport.objects.bulk_create(objs)

    return JsonResponse({
        "status": "success",
        "inserted": len(objs)
    })


def get_stock_report(request):
    data = list(
        StockReport.objects.values(
            "code", "name", "productcode", "barcode", "bmrp", "salesprice", "quantity"
        )
    )

    return JsonResponse({
        "status": "success",
        "count": len(data),
        "data": data
    })
