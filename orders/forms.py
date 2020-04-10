from django import forms
from . import models


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['first_name', 'last_name', 'email',
                  'address', 'postal_code', 'city']
