import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AccSalesType


@csrf_exempt
def upload_acc_sales_types(request):
    data = json.loads(request.body or "[]")

    AccSalesType.objects.all().delete()

    objs = [
        AccSalesType(
            cd=row.get("cd"),
            name=row.get("name")
        )
        for row in data
        if row.get("cd")
    ]

    AccSalesType.objects.bulk_create(objs)

    return JsonResponse({
        "status": "success",
        "inserted": len(objs)
    })


def get_acc_sales_types(request):
    data = list(
        AccSalesType.objects.values("cd", "name")
    )

    return JsonResponse({
        "status": "success",
        "count": len(data),
        "data": data
    })
