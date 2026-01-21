from django.urls import path
from .views import pdc_api

urlpatterns = [
    path("pdc/", pdc_api, name="pdc_api"),
]
