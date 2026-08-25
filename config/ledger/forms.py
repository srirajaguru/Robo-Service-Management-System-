from django import forms

from .models import Expense, Payment


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["description", "amount"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["amount", "payment_method", "reference_number"]
