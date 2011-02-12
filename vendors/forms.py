import django.forms as forms
from vendors.models import Vendor
from django.db.models import TextField

class VendorForm(forms.ModelForm):
    class Meta:
        model=Vendor
        exclude=('public','owner', 'markets', 'slug',)

    def save(self, commit=True):
        f = super(VendorForm, self).save(commit=False)
        if not f.pk: f.owner = request.user
        if commit: f.save()
        return f
                                                                
        
class MarketSignUpForm(forms.ModelForm):
    #cal = Calendar.objects.get(slug__exact='castine-farmers-market')
    #markets = forms.ModelMultipleChoiceField(cal.events.all(), widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model=Vendor
        fields=('markets')
        
