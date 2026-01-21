from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RefreshTag


@api_view(["POST"])
def upload_refresh_tag(request):
    client_id = request.GET.get("client_id")

    if not client_id:
        return Response({"error": "client_id required"}, status=400)

    data = request.data
    if not isinstance(data, list):
        return Response({"error": "Expected list"}, status=400)

    # clear old client data
    RefreshTag.objects.filter(client_id=client_id).delete()

    objs = []
    for row in data:
        objs.append(
            RefreshTag(
                client_id=client_id,
                edate=row.get("edate"),
                etime=row.get("etime"),
                userid=row.get("userid"),
                remark=row.get("remark"),
            )
        )

    RefreshTag.objects.bulk_create(objs, batch_size=1000)

    return Response({
        "success": True,
        "count": len(objs)
    })


@api_view(["GET"])
def get_refresh_tag(request):
    client_id = request.GET.get("client_id")

    qs = RefreshTag.objects.all()
    if client_id:
        qs = qs.filter(client_id=client_id)

    data = list(qs.values())
    return Response(data)
