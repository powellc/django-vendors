from django.forms import ModelForm
from vendors.models import Vendor

class VendorForm(ModelForm):
    class Meta:
        model=Vendor
        exclude=('public','owner', 'slug','markets',)
