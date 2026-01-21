from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PDC


@api_view(["POST"])
def upload_pdc(request):
    client_id = request.GET.get("client_id")
    data = request.data

    PDC.objects.filter(client_id=client_id).delete()

    objs = [
        PDC(
            client_id=client_id,
            colndate=row.get("colndate"),
            party=row.get("party"),
            amount=row.get("amount"),
            chequedate=row.get("chequedate"),
            chequeno=row.get("chequeno"),
            colnstatus=row.get("colnstatus"),
            status=row.get("status"),
        )
        for row in data
    ]

    PDC.objects.bulk_create(objs)
    return Response({"success": True, "count": len(objs)})
