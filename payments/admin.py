from django.contrib import admin

from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'created_time')
