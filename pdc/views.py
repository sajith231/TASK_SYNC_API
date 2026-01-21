from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import PDC


@api_view(["POST"])
def upload_pdc(request):
    """
    Upload PDC data
    client_id MUST be sent in request body
    """

    client_id = request.data.get("client_id")
    rows = request.data.get("data", [])

    if not client_id:
        return Response(
            {"success": False, "message": "client_id is required"},
            status=400
        )

    if not isinstance(rows, list):
        return Response(
            {"success": False, "message": "data must be a list"},
            status=400
        )

    # 🔥 Clear existing client data
    PDC.objects.filter(client_id=client_id).delete()

    objs = []

    for row in rows:
        objs.append(
            PDC(
                client_id=client_id,

                # Dates can come as ISO strings (YYYY-MM-DD)
                colndate=row.get("colndate"),
                chequedate=row.get("chequedate"),

                party=row.get("party"),
                amount=row.get("amount"),
                chequeno=row.get("chequeno"),
                colnstatus=row.get("colnstatus"),
                status=row.get("status"),
            )
        )

    # 🔥 Bulk insert
    PDC.objects.bulk_create(objs)

    return Response({
        "success": True,
        "client_id": client_id,
        "count": len(objs)
    })
