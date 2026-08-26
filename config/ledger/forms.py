from decimal import Decimal
from django import forms
from .models import Expense, Payment, Invoice


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'description', 'amount']
        widgets = {
            'expense_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 8GB DDR4 RAM / Power IC / New Keyboard',
                'required': True,
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount in ₹',
                'step': '0.01',
                'min': '0',
                'required': True,
            }),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'reference_number', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Payment amount ₹',
                'step': '0.01',
                'min': '0.01',
                'required': True,
            }),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UPI Ref / Transaction ID / Slip No (Optional)',
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional remarks (e.g. Advance paid / Final settlement)',
            }),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['labor_charge', 'parts_charge', 'other_charges', 'discount', 'notes']
        widgets = {
            'labor_charge': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'parts_charge': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'other_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional invoice notes / warranty remarks'}),
        }

    def clean_labor_charge(self):
        charge = self.cleaned_data.get('labor_charge')
        return charge if charge is not None else Decimal('0.00')

    def clean_parts_charge(self):
        charge = self.cleaned_data.get('parts_charge')
        return charge if charge is not None else Decimal('0.00')

    def clean_other_charges(self):
        charge = self.cleaned_data.get('other_charges')
        return charge if charge is not None else Decimal('0.00')

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        return discount if discount is not None else Decimal('0.00')
