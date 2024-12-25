from django.contrib import admin

from .models import Payment, OutboxPayment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'status', 'create_at', 'update_at')
    search_fields = ('id',  'order_id', 'status', 'create_at', 'update_at')
    list_filter = ('status', 'create_at', 'update_at')


@admin.register(OutboxPayment)
class OutboxPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic_name', 'status', 'create_at', 'update_at')
