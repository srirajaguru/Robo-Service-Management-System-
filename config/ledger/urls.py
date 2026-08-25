from django.urls import path

from .views import expense_create, ledger_list, payment_create

urlpatterns = [
	path("", ledger_list, name="ledger_list"),
	path("<int:service_id>/expense/", expense_create, name="expense_create"),
	path("<int:service_id>/payment/", payment_create, name="payment_create"),
]
