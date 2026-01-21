from django.urls import path
from .views import upload_eventlog

urlpatterns = [
    path("upload-eventlog/", upload_eventlog),
]