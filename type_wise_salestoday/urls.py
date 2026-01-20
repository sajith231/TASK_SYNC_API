from django.urls import path
from .views import (
    UploadTypeWiseSalesTodayAPI,
    GetTypeWiseSalesTodayAPI
)

urlpatterns = [
    path('upload-type-wise-sales-today/', UploadTypeWiseSalesTodayAPI.as_view()),
    path('get-type-wise-sales-today/', GetTypeWiseSalesTodayAPI.as_view()),
]
