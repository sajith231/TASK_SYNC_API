import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import TenderCash


# ===============================
# 🔥 UPLOAD TENDERCASH
# ===============================
@csrf_exempt
@require_http_methods(["POST"])
def upload_tendercash(request):
    client_id = request.GET.get("client_id")

    if not client_id:
        return JsonResponse(
            {"error": "client_id is required"},
            status=400
        )

    try:
        payload = json.loads(request.body or b"[]")
    except Exception:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    if not isinstance(payload, list):
        return JsonResponse(
            {"error": "Expected a list of records"},
            status=400
        )

    # 🔥 Clear old client data
    TenderCash.objects.filter(client_id=client_id).delete()

    objs = []
    for row in payload:
        objs.append(
            TenderCash(
                client_id=client_id,
                mslno=row.get("mslno"),
                tender_code=row.get("tender_code"),
                amount=row.get("amount"),
                currency_code=row.get("currency_code"),
                currency_name=row.get("currency_name"),
            )
        )

    TenderCash.objects.bulk_create(objs, batch_size=500)

    return JsonResponse({
        "status": "success",
        "client_id": client_id,
        "inserted": len(objs)
    }, status=201)


# ===============================
# 🔥 GET TENDERCASH
# ===============================
@require_http_methods(["GET"])
def get_tendercash(request):
    client_id = request.GET.get("client_id")

    if not client_id:
        return JsonResponse(
            {"error": "client_id is required"},
            status=400
        )

    qs = TenderCash.objects.filter(client_id=client_id)

    data = list(qs.values(
        "mslno",
        "tender_code",
        "amount",
        "currency_code",
        "currency_name"
    ))

    return JsonResponse({
        "client_id": client_id,
        "count": len(data),
        "data": data
    })
