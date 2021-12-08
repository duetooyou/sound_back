from django.contrib import admin
from .models import Company, Record, Studio


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'company_logo', 'active_now', )
    list_filter = ('active_now',)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'city', 'address')
    list_filter = ('company', 'city')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_filter = ('studio', 'cost', 'session_cost', 'start_recording')
    list_filter = ('studio', 'cost', 'session_cost', 'start_recording')
    search_fields = ('studio',)
