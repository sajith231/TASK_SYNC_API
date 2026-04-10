from django.urls import path
from .views import (
    UploadAccUsersAPI, GetAccUsersAPI,
    UploadMiselAPI, GetMiselAPI,
    UploadAccMasterAPI, GetAccMasterAPI,
    UploadAccLedgersAPI, GetAccLedgersAPI,
    UploadAccInvmastAPI, GetAccInvmastAPI,
    UploadCashAndBankAccMasterAPI, GetCashAndBankAccMasterAPI,
    # NEW imports
    UploadAccTtServicemasterAPI, GetAccTtServicemasterAPI,
    UploadSalesTodayAPI, GetSalesTodayAPI,
    UploadPurchaseTodayAPI, GetPurchaseTodayAPI,

    UploadSalesDaywiseAPI, GetSalesDaywiseAPI,
    UploadSalesMonthwiseAPI, GetSalesMonthwiseAPI,
    UploadSalesReturnReportAPI, GetSalesReturnReportAPI,
    UploadPurchaseDaywiseAPI, GetPurchaseDaywiseAPI,
    UploadPurchaseMonthwiseAPI, GetPurchaseMonthwiseAPI,
    
)


urlpatterns = [
    path('upload-users/', UploadAccUsersAPI.as_view(), name='upload_users'),
    path('get-users/', GetAccUsersAPI.as_view(), name='get_users'),
    path('upload-misel/', UploadMiselAPI.as_view(), name='upload_misel'),
    path('get-misel/', GetMiselAPI.as_view(), name='get_misel'),

    path('upload-acc-master/', UploadAccMasterAPI.as_view(), name='upload_acc_master'),
    path('get-acc-master/', GetAccMasterAPI.as_view(), name='get_acc_master'),
    path('upload-acc-ledgers/', UploadAccLedgersAPI.as_view(), name='upload_acc_ledgers'),
    path('get-acc-ledgers/', GetAccLedgersAPI.as_view(), name='get_acc_ledgers'),
    path('upload-acc-invmast/', UploadAccInvmastAPI.as_view(), name='upload_acc_invmast'),
    path('get-acc-invmast/', GetAccInvmastAPI.as_view(), name='get_acc_invmast'),

    path('upload-cashandbankaccmaster/', UploadCashAndBankAccMasterAPI.as_view(), name='upload_cashandbankaccmaster'),
    path('get-cashandbankaccmaster/', GetCashAndBankAccMasterAPI.as_view(), name='get_cashandbankaccmaster'),

    # NEW end-points
    path('upload-accttservicemaster/', UploadAccTtServicemasterAPI.as_view(), name='upload_accttservicemaster'),
    path('get-accttservicemaster/',    GetAccTtServicemasterAPI.as_view(),    name='get_accttservicemaster'),
    path('upload-sales-today/', UploadSalesTodayAPI.as_view(), name='upload_sales_today'),
    path('get-sales-today/', GetSalesTodayAPI.as_view(), name='get_sales_today'),
    path('upload-purchase-today/', UploadPurchaseTodayAPI.as_view(), name='upload_purchase_today'),
    path('get-purchase-today/', GetPurchaseTodayAPI.as_view(), name='get_purchase_today'),



    path('upload-sales-daywise/', UploadSalesDaywiseAPI.as_view(), name='upload_sales_daywise'),
    path('get-sales-daywise/', GetSalesDaywiseAPI.as_view(), name='get_sales_daywise'),
    path('upload-sales-monthwise/', UploadSalesMonthwiseAPI.as_view(), name='upload_sales_monthwise'),
    path('get-sales-monthwise/', GetSalesMonthwiseAPI.as_view(), name='get_sales_monthwise'),

    path('upload-salesreturn-report/', UploadSalesReturnReportAPI.as_view(), name='upload_salesreturn_report'),
    path('get-salesreturn-report/', GetSalesReturnReportAPI.as_view(), name='get_salesreturn_report'),
    path('upload-purchase-daywise/', UploadPurchaseDaywiseAPI.as_view(), name='upload_purchase_daywise'),
    path('get-purchase-daywise/', GetPurchaseDaywiseAPI.as_view(), name='get_purchase_daywise'),
    path('upload-purchase-monthwise/', UploadPurchaseMonthwiseAPI.as_view(), name='upload_purchase_monthwise'),
    path('get-purchase-monthwise/', GetPurchaseMonthwiseAPI.as_view(), name='get_purchase_monthwise'),

]
# xha