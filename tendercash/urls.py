from django.urls import path
from .views import upload_tendercash, get_tendercash

urlpatterns = [
    path("upload-tendercash/", upload_tendercash, name="upload_tendercash"),
    path("get-tendercash/", get_tendercash, name="get_tendercash"),
]
