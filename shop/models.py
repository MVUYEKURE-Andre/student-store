"""
Database models for the shop app.

Product  — items for sale (managed via Django admin).
Order    — a customer's purchase (created at checkout).
OrderItem — one line on an order (product + quantity + price snapshot).
"""

from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    """An item available in the store."""

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="URL to a product image")
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Order(models.Model):
    """A customer order placed at checkout."""

    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} — {self.customer_name}"

    @property
    def total(self):
        """Sum of all line items on this order."""
        return sum(item.line_total for item in self.items.all())


class OrderItem(models.Model):
    """One product line on an order (price is saved at purchase time)."""

    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def line_total(self):
        return self.price_at_purchase * self.quantity


class OrderStatusHistory(models.Model):
    """Tracks status changes for an order over time."""

    order = models.ForeignKey(
        Order, related_name="status_history", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["changed_at"]

    def __str__(self):
        return f"Order #{self.order_id} -> {self.get_status_display()} at {self.changed_at}"


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def create_initial_order_status_history(sender, instance, created, **kwargs):
    if created:
        OrderStatusHistory.objects.create(order=instance, status=instance.status)
