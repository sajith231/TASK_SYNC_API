from django.urls import path
from .views import UploadStockSummaryAPI, GetStockSummaryAPI
 
urlpatterns = [
    path("upload-stock-summary/", UploadStockSummaryAPI.as_view(), name="upload_stock_summary"),
    path("get-stock-summary/",    GetStockSummaryAPI.as_view(),    name="get_stock_summary"),
]
 


















