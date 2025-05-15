from django import forms
from .models import Transaction, Product

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '1'})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'description', 'price', 'stock', 'status']
        exclude = ['owner']
        widgets = {
            'product_type': forms.Select(),
            'status': forms.Select(),
        }
