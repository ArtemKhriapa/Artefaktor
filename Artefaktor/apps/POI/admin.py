from django.contrib import admin
from .models import  GisPOI, Category
from django_mptt_admin.admin import DjangoMpttAdmin

class CategoryAdmin(DjangoMpttAdmin):
        pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(GisPOI)
#admin.site.register(Category)
