from decimal import Decimal
from django import forms
from customers.models import Customer
from .models import Service, ServiceProgress


class ServiceInwardForm(forms.ModelForm):
    # Quick accessories options for checkboxes
    ACCESSORY_PRESETS = [
        ('Charger / Adapter', 'Charger / Power Adapter'),
        ('Power Cable', 'Power Cable'),
        ('Battery', 'Battery'),
        ('Laptop Bag / Sleeve', 'Laptop Bag / Sleeve'),
        ('Mouse', 'Mouse'),
        ('Keyboard', 'Keyboard'),
        ('Cartridge / Toner', 'Cartridge / Toner'),
        ('Original Box', 'Original Box'),
        ('Other', 'Other Accessories'),
    ]

    selected_accessories = forms.MultipleChoiceField(
        choices=ACCESSORY_PRESETS,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    custom_accessories = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Additional accessories or serial details'
        })
    )

    class Meta:
        model = Service
        fields = [
            'customer', 'device_type', 'brand', 'model', 'serial_number', 'asset_number',
            'physical_condition', 'complaint', 'initial_diagnosis', 'technician_notes',
            'priority', 'expected_completion_date', 'estimated_cost', 'service_charge'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select', 'required': True, 'id': 'id_customer_select'}),
            'device_type': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dell, HP, Lenovo, Canon, Epson', 'required': True}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Inspiron 15 3511 / L3110 / Dome 2MP', 'required': True}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number / Service Tag'}),
            'asset_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Office Asset / Internal Tag ID'}),
            'physical_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Minor scratches on base, hinges intact'}),
            'complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detailed customer complaint / issue description', 'required': True}),
            'initial_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Initial inspection findings by technician'}),
            'technician_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Internal notes (optional)'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'expected_completion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated ₹', 'step': '0.01'}),
            'service_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Service Charge ₹', 'step': '0.01'}),
        }

    def clean_estimated_cost(self):
        cost = self.cleaned_data.get('estimated_cost')
        return cost if cost is not None else Decimal('0.00')

    def clean_service_charge(self):
        charge = self.cleaned_data.get('service_charge')
        return charge if charge is not None else Decimal('0.00')

    def clean(self):
        cleaned_data = super().clean()
        presets = cleaned_data.get('selected_accessories') or []
        custom = cleaned_data.get('custom_accessories') or ''
        parts = list(presets)
        if custom.strip():
            parts.append(custom.strip())
        cleaned_data['accessories'] = ", ".join(parts) if parts else "None"
        return cleaned_data


class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'device_type', 'brand', 'model', 'serial_number', 'asset_number',
            'physical_condition', 'accessories', 'complaint', 'initial_diagnosis',
            'technician_notes', 'priority', 'expected_completion_date',
            'service_charge', 'discount'
        ]
        widgets = {
            'device_type': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'asset_number': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_condition': forms.TextInput(attrs={'class': 'form-control'}),
            'accessories': forms.TextInput(attrs={'class': 'form-control'}),
            'complaint': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'initial_diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'technician_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'expected_completion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'service_charge': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_service_charge(self):
        charge = self.cleaned_data.get('service_charge')
        return charge if charge is not None else Decimal('0.00')

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        return discount if discount is not None else Decimal('0.00')


class StatusUpdateForm(forms.Form):
    status = forms.ChoiceField(
        choices=Service.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional status transition remarks'
        })
    )


class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceProgress
        fields = ['progress_description']
        widgets = {
            'progress_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe current technical inspection / repair progress...',
                'required': True,
            })
        }
