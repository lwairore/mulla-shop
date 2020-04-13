from django import forms
from . import models
from localflavor.us.forms import USZipCodeField


class OrderCreateForm(forms.ModelForm):
    postal_code = USZipCodeField()

    class Meta:
        model = models.Order
        fields = ['first_name', 'last_name', 'email',
                  'address', 'postal_code', 'city']
