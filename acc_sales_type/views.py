import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AccSalesType


@csrf_exempt
def upload_acc_sales_types(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    client_id = request.GET.get("client_id")
    if not client_id:
        return JsonResponse({"error": "client_id required"}, status=400)

    try:
        data = json.loads(request.body or "[]")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # ✅ Delete only THIS client's data
    AccSalesType.objects.filter(client_id=client_id).delete()

    objs = [
        AccSalesType(
            cd=row.get("cd"),
            name=row.get("name"),
            client_id=client_id
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
    client_id = request.GET.get("client_id")

    qs = AccSalesType.objects.all()
    if client_id:
        qs = qs.filter(client_id=client_id)

    data = list(qs.values("cd", "name"))

    return JsonResponse({
        "status": "success",
        "count": len(data),
        "data": data
    })
