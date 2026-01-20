from django.urls import path
from . import views

urlpatterns = [
    path("upload-acc-sales-types/", views.upload_acc_sales_types),
    path("get-acc-sales-types/", views.get_acc_sales_types),
]
