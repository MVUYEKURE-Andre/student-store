"""Email helpers for order notifications."""

import resend
from django.conf import settings


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
    try:
        api_key = getattr(settings, "RESEND_API_KEY", None)
        if not api_key:
            print("RESEND_API_KEY not configured. Skipping admin notification.", flush=True)
            return
        resend.api_key = api_key
        resend.Emails.send({
            "from": getattr(settings, "DEFAULT_FROM_EMAIL", "onboarding@resend.dev"),
            "to": ["etelevel463@gmail.com"],
            "subject": f"New order #{order.pk} received",
            "text": _build_order_summary(order),
        })
    except Exception as exc:
        print(f"RESEND ADMIN NOTIFICATION ERROR: {exc}", flush=True)


def send_order_confirmation(order) -> None:
    """Notify the customer when their order is confirmed."""
    try:
        api_key = getattr(settings, "RESEND_API_KEY", None)
        if not api_key or not order.customer_email:
            return
        resend.api_key = api_key
        resend.Emails.send({
            "from": getattr(settings, "DEFAULT_FROM_EMAIL", "onboarding@resend.dev"),
            "to": [order.customer_email],
            "subject": f"Order Confirmation - Order #{order.pk}",
            "text": (
                f"Hello {order.customer_name},\n\n"
                f"Thank you for your order!\n\n"
                f"{_build_order_summary(order)}"
            ),
        })
    except Exception as exc:
        print(f"RESEND ORDER CONFIRMATION ERROR: {exc}", flush=True)


def send_order_status_update(order) -> None:
    """Notify the customer when an order status changes."""
    try:
        api_key = getattr(settings, "RESEND_API_KEY", None)
        if not api_key or not order.customer_email:
            return
        resend.api_key = api_key
        resend.Emails.send({
            "from": getattr(settings, "DEFAULT_FROM_EMAIL", "onboarding@resend.dev"),
            "to": [order.customer_email],
            "subject": f"Your order #{order.pk} is now {order.get_status_display()}",
            "text": (
                f"Hello {order.customer_name},\n\n"
                f"Your order #{order.pk} is now {order.get_status_display()}.\n\n"
                f"Total: ${order.total}\n"
                f"Email: {order.customer_email}"
            ),
        })
    except Exception as exc:
        print(f"RESEND STATUS UPDATE ERROR: {exc}", flush=True)