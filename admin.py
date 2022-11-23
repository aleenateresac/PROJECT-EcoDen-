from django.contrib import admin
from . models import Account
from django.http import HttpResponse
import csv
from django.contrib.auth.admin import UserAdmin
from .models import product
from .models import productcustomer
from .models import dumb
# from django.contrib.auth.models import Group,User


# #  Register your models here.
admin.site.site_header="EcoDen"
admin.site.site_title="Welcome To Admin's Dashboard"
admin.site.index_title="Welcome to EcoDen Dashboard"
# admin.site.register(Account)
admin.site.register(product)
admin.site.register(productcustomer)
admin.site.register(dumb)



def export_reg(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="registration.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name','Email','Address', 'Phone', 'State','City','Pincode'])
        registration = queryset.values_list('name','email','address', 'phone', 'state','city','pincode')
        for i in registration:
            writer.writerow(i)
        return response


export_reg.short_description = 'Export to csv'

class Regdetailes(admin.ModelAdmin):
    list_display = ['name','email','address','phone', 'state','city','pincode']
    actions = [export_reg]


admin.site.register(Account,Regdetailes)


class AccountAdmin(UserAdmin):
    list_display = ['name','lname','email','phone','address','city','state','pincode','status']
    ordering=('name',)
    search_fields = ('name','email')
    filter_horizontal = ()
    list_per_page = 50
    list_filter = ('name','email')
    filedsets=()
    list_display_links = ('email')

    




class productadmin(admin.ModelAdmin):
    list_display = ['product_image','product_description']

class productcustomeradmin(admin.ModelAdmin):
    list_display = ['product_image','product_name','product_description','product_price']


