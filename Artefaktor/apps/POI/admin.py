from django.contrib import admin
from .models import  GisPOI, DraftGisPOI ,Category
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin

class CategoryAdmin(DjangoMpttAdmin):
    pass


# func for do something with obj in queryset
def make_poi(modeladmin, request, queryset):
    for obj in queryset:
        print('I whant to do something with: ',obj.id)

make_poi.short_description = "Approve DraftPOI as POI" # description for action 'make_poi'


class DraftGisPOIAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'is_moderate']
    actions = [make_poi]


admin.site.register(Category, CategoryAdmin)
admin.site.register(GisPOI)
admin.site.register(DraftGisPOI, DraftGisPOIAdmin)
