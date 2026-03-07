from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .models import TypeWiseSalesToday
import logging, traceback

logger = logging.getLogger(__name__)


class UploadTypeWiseSalesTodayAPI(APIView):
    """
    Upload TYPE wise sales summary for TODAY
    """

    def post(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "client_id required"}, status=400)

        try:
            # clear old data
            TypeWiseSalesToday.objects.filter(client_id=client_id).delete()

            query = """
                SELECT 
                    type AS TYPE,
                    SUM(nettotal) AS NETTOTAL,
                    COUNT(*) AS BILLCOUNT
                FROM acc_invmast
                WHERE billno > 0
                AND invdate = CURRENT DATE
                GROUP BY type
            """

            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            bulk = []
            for r in rows:
                bulk.append(TypeWiseSalesToday(
                    type=r[0],
                    nettotal=r[1],
                    billcount=r[2],
                    client_id=client_id
                ))

            TypeWiseSalesToday.objects.bulk_create(bulk)

            return Response({
                "message": "Type wise sales today synced",
                "records": len(bulk)
            }, status=201)

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response({"error": str(e)}, status=500)


class GetTypeWiseSalesTodayAPI(APIView):
    """
    Get TYPE wise sales today
    """

    def get(self, request):
        client_id = request.query_params.get('client_id')

        if not client_id:
            return Response({"error": "client_id required"}, status=400)

        qs = TypeWiseSalesToday.objects.filter(client_id=client_id)

        data = [{
            "TYPE": i.type,
            "NETTOTAL": str(i.nettotal),
            "BILLCOUNT": i.billcount
        } for i in qs]

        return Response({
            "count": len(data),
            "data": data
        }, status=200)
