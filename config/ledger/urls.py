from django.urls import path
from .views import (
    ledger_list, expense_create, expense_delete, payment_create,
    invoice_view, reports_monthly, export_monthly_csv, reports_yearly, export_yearly_csv
)

urlpatterns = [
    path('', ledger_list, name='ledger_list'),
    path('<int:service_id>/expense/', expense_create, name='expense_create'),
    path('expense/<int:expense_id>/delete/', expense_delete, name='expense_delete'),
    path('<int:service_id>/payment/', payment_create, name='payment_create'),
    path('<int:service_id>/invoice/', invoice_view, name='invoice_view'),
    path('reports/monthly/', reports_monthly, name='reports_monthly'),
    path('reports/monthly/export/', export_monthly_csv, name='export_monthly_csv'),
    path('reports/yearly/', reports_yearly, name='reports_yearly'),
    path('reports/yearly/export/', export_yearly_csv, name='export_yearly_csv'),
]
