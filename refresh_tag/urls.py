from django.urls import path
from .views import upload_refresh_tag, get_refresh_tag

urlpatterns = [
    path("upload-refresh-tag/", upload_refresh_tag),
    path("get-refresh-tag/", get_refresh_tag),
]