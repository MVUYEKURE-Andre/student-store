"""Email helpers for order notifications."""

from django.conf import settings
from django.core.mail import send_mail


def _build_order_summary(order) -> str:
    lines = [
        f"Order #{order.pk}",
        f"Customer: {order.customer_name}",
        f"Email: {order.customer_email}",
        f"Status: {order.get_status_display()}",
        "",
        "Items:",
    ]
    for item in order.items.select_related("product").all():
        lines.append(f"- {item.quantity}x {item.product.name} @ ${item.price_at_purchase} = ${item.line_total}")
    lines.append("")
    lines.append(f"Total: ${order.total}")
    return "\n".join(lines)


def send_new_order_notification(order) -> None:
    """Notify the admin when a new order is placed."""
    send_mail(
        subject=f"New order #{order.pk} received",
        message=_build_order_summary(order),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["etelevel463@gmail.com"],
        fail_silently=False,
    )


def send_order_status_update(order) -> None:
    """Notify the customer when an order status changes."""
    send_mail(
        subject=f"Your order #{order.pk} is now {order.get_status_display()}",
        message=(
            f"Hello {order.customer_name},\n\n"
            f"Your order #{order.pk} is now {order.get_status_display()}.\n\n"
            f"Total: ${order.total}\n"
            f"Email: {order.customer_email}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.customer_email],
        fail_silently=False,
    )