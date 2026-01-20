
from django.urls import path
from .views import upload_stock_report, get_stock_report

urlpatterns = [
    path("upload-stock-report/", upload_stock_report, name="upload_stock_report"),
    path("get-stock-report/", get_stock_report, name="get_stock_report"),
]