"""
Django admin configuration — register models so you can manage
products and orders at /admin without writing code.
"""

from django.contrib import admin

from .email_utils import send_order_status_update
from .models import Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product list shows name, price, stock, and when it was added."""

    list_display = ("name", "price", "stock_quantity", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description")
    ordering = ("name",)


class OrderItemInline(admin.TabularInline):
    """Show order line items directly on the order edit page."""

    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price_at_purchase")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order list shows customer info, date, payment status, and total."""

    list_display = (
        "id",
        "customer_name",
        "customer_email",
        "user",
        "order_total",
        "status",
        "created_at",
    )
    list_display_links = ("id", "customer_name")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_email")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at",)
    list_select_related = ("user",)

    @admin.display(description="Total")
    def order_total(self, obj):
        return f"${obj.total:.2f}"

    def save_model(self, request, obj, form, change):
        old_status = None
        if change and obj.pk:
            old_status = Order.objects.filter(pk=obj.pk).values_list("status", flat=True).first()

        super().save_model(request, obj, form, change)

        if change and old_status and old_status != obj.status and obj.customer_email:
            try:
                send_order_status_update(obj)
            except Exception as exc:
                print("ORDER STATUS EMAIL ERROR:", exc, flush=True)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Standalone view for individual order line items."""

    list_display = ("order", "product", "quantity", "price_at_purchase", "line_total_display")
    list_filter = ("order__created_at",)

    @admin.display(description="Line total")
    def line_total_display(self, obj):
        return f"${obj.line_total:.2f}"
