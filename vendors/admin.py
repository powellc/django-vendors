from vendors.models import Vendor
from django.contrib import admin

class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display  = ['name', 'town','public', 'created', 'updated']
    list_filter   = ['town', 'public', 'markets']
    ordering = ['-created']
    search_fields = ['name', 'description']
    date_hierarchy='created'
    
admin.site.register(Vendor, VendorAdmin)
