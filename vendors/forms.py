import django.forms as forms
from django.forms import ModelForm
from vendors.models import Vendor, Application
from schedule.models import Calendar, Event
from tagging.fields import TagField
from django.db.models import TextField

class VendorForm(ModelForm):
    class Meta:
        model=Vendor
        exclude=('public','owner', 'markets', 'slug','lat_long')
        
class VendorAppForm(ModelForm):
    class Meta:
        model=Application
        exclude=('signed_bylaws','submission_date', 'approval_date', 'insurance_on_file', )        
        
class MarketSignUpForm(ModelForm):
    #cal = Calendar.objects.get(slug__exact='castine-farmers-market')
    #markets = forms.ModelMultipleChoiceField(cal.events.all(), widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model=Vendor
        fields=('markets')
        
