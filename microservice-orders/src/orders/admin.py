from django.contrib import admin

from .models import Order, OutboxOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'create_at', 'update_at')
    search_fields = ('id', 'user', 'status', 'create_at', 'update_at')
    list_filter = ('status', 'create_at', 'update_at')


@admin.register(OutboxOrder)
class OutboxOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic_name', 'status', 'create_at', 'update_at')
