from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EventLog


@api_view(["POST"])
def upload_eventlog(request):
    client_id = request.data.get("client_id")
    data = request.data.get("data", [])

    # Clear old
    EventLog.objects.filter(client_id=client_id).delete()

    objs = [
        EventLog(
            client_id=client_id,
            uid=row["uid"],
            edate=row["edate"],
            etime=row["etime"],
            sevent=row["sevent"],
        )
        for row in data
    ]

    EventLog.objects.bulk_create(objs)
    return Response({"success": True, "count": len(objs)})
