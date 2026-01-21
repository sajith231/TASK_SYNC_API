from django.urls import path
from .views import upload_pdc

urlpatterns = [
    path("upload-pdc/", upload_pdc, name="upload_pdc"),
]
