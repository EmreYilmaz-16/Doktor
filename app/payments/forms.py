from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_type', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Açıklama (isteğe bağlı)'}),
        }
