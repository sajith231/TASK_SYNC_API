from django.urls import path
from . import views

urlpatterns = [
    path("upload-stock-report/", views.upload_stock_report),
    path("get-stock-report/", views.get_stock_report),
]
