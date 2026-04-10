from django.shortcuts import render

# Create your views here.
import logging
import traceback

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StockSummary

logger = logging.getLogger(__name__)


# ===============================
# UPLOAD  (POST)
# ===============================
class UploadStockSummaryAPI(APIView):
    """
    POST /api/upload-stock-summary/?client_id=<id>

    Expected JSON body (single dict, NOT a list):
    {
        "total_products":    1250,
        "total_stock_value": 987654.321,
        "barcode_mode":      false
    }

    Upserts one row per client_id (delete-then-insert).
    """

    def post(self, request):
        data      = request.data
        client_id = request.query_params.get("client_id")

        if not client_id:
            return Response(
                {"error": "Missing client_id in query parameters."},
                status=400,
            )

        if not isinstance(data, dict):
            return Response(
                {"error": "Expected a JSON object (dict), not a list."},
                status=400,
            )

        # Validate required fields
        required = ("total_products", "total_stock_value")
        missing = [f for f in required if f not in data]
        if missing:
            return Response(
                {"error": f"Missing required field(s): {', '.join(missing)}"},
                status=400,
            )

        try:
            # One summary row per client — always replace
            StockSummary.objects.filter(client_id=client_id).delete()

            StockSummary.objects.create(
                total_products    = int(data.get("total_products", 0)),
                total_stock_value = data.get("total_stock_value", 0),
                barcode_mode      = bool(data.get("barcode_mode", False)),
                client_id         = client_id,
            )

            return Response(
                {
                    "message": (
                        f"Stock summary uploaded for client_id {client_id}. "
                        f"Products: {data.get('total_products')}, "
                        f"Value: {data.get('total_stock_value')}"
                    )
                },
                status=201,
            )

        except Exception as e:
            logger.error(
                f"Error in UploadStockSummaryAPI: {e}\n{traceback.format_exc()}"
            )
            return Response({"error": str(e)}, status=500)


# ===============================
# GET  (GET)
# ===============================
class GetStockSummaryAPI(APIView):
    """
    GET /api/get-stock-summary/?client_id=<id>

    Returns:
    {
        "client_id": "...",
        "total_products": 1250,
        "total_stock_value": "987654.321",
        "barcode_mode": false
    }
    """

    def get(self, request):
        client_id = request.query_params.get("client_id")

        if not client_id:
            return Response(
                {"error": "Missing client_id in query parameters."},
                status=400,
            )

        try:
            summary = StockSummary.objects.get(client_id=client_id)
        except StockSummary.DoesNotExist:
            return Response(
                {"error": f"No stock summary found for client_id {client_id}."},
                status=404,
            )

        return Response(
            {
                "client_id":         client_id,
                "total_products":    summary.total_products,
                "total_stock_value": str(summary.total_stock_value),
                "barcode_mode":      summary.barcode_mode,
            },
            status=200,
        )