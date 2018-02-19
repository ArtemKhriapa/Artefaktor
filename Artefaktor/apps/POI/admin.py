from django.contrib import admin
from .models import  GisPOI, Category
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin

class CategoryAdmin( DjangoMpttAdmin):  # MPTTModelAdmin):
        pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(GisPOI)
#admin.site.register(Category)
