"""
Views for the shop — each function handles one page or action.
"""

import resend
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignupForm, StyledAuthenticationForm
from .cart import (
    add_to_cart,
    clear_cart,
    get_cart_items,
    remove_from_cart,
    update_cart_item,
)
from .email_utils import send_new_order_notification, send_order_confirmation
from .models import Order, OrderItem, Product


def home(request):
    """Homepage — grid of all products."""
    products = Product.objects.filter(stock_quantity__gt=0)
    return render(request, "shop/home.html", {"products": products})


def about(request):
    """About page — short description of the store."""
    return render(request, "shop/about.html")


def services(request):
    """Services page — explains how the store works."""
    return render(request, "shop/services.html")


class ShopLoginView(LoginView):
    """Styled login view that shows a success message after login."""

    template_name = "registration/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return response


def signup(request):
    """Create a new user account and sign them in."""
    if request.user.is_authenticated:
        return redirect("shop:home")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("shop:home")
    else:
        form = SignupForm()

    return render(request, "shop/signup.html", {"form": form})


def logout_view(request):
    """Log the visitor out and return to the homepage."""
    username = request.user.username if request.user.is_authenticated else "there"
    auth_logout(request)
    messages.success(request, f"Goodbye, {username}! You have been logged out.")
    return redirect("shop:home")


def contact(request):
    """Contact page with a simple form and success message."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(request, "Please fill in all contact form fields.")
        else:
            subject = f"Student Store contact form: {name}"
            body = (
                f"Name: {name}\n"
                f"Email: {email}\n\n"
                f"Message:\n{message}"
            )

            try:
                api_key = getattr(settings, "RESEND_API_KEY", None)
                if api_key:
                    resend.api_key = api_key
                    resend.Emails.send({
                        "from": getattr(settings, "DEFAULT_FROM_EMAIL", "onboarding@resend.dev"),
                        "to": ["etelevel463@gmail.com"],
                        "subject": subject,
                        "text": body,
                    })
                messages.success(request, "Thanks for reaching out. We'll get back to you soon.")
                return redirect("shop:contact")
            except Exception as exc:
                print("CONTACT EMAIL ERROR:", exc, flush=True)
                messages.error(request, f"Could not send message: {exc}")

    return render(request, "shop/contact.html")


def product_detail(request, product_id):
    """Single product page with full description."""
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "shop/product_detail.html", {"product": product})


def cart_add(request, product_id):
    """Add a product to the cart and redirect back."""
    product = get_object_or_404(Product, pk=product_id)
    if product.stock_quantity < 1:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect("shop:home")

    add_to_cart(request.session, product_id)
    messages.success(request, f"Added {product.name} to your cart.")
    next_url = request.POST.get("next", "shop:home")
    if next_url.startswith("/"):
        return redirect(next_url)
    return redirect("shop:product_detail", product_id=product_id)


def cart_view(request):
    """Cart page — list items, quantities, and total."""
    items, total = get_cart_items(request.session)
    return render(
        request,
        "shop/cart.html",
        {"cart_items": items, "cart_total": total},
    )


def cart_update(request, product_id):
    """Update quantity for a cart item (POST only)."""
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        update_cart_item(request.session, product_id, quantity)
    return redirect("shop:cart")


def cart_remove(request, product_id):
    """Remove an item from the cart."""
    remove_from_cart(request.session, product_id)
    messages.info(request, "Item removed from cart.")
    return redirect("shop:cart")


def checkout(request):
    """Checkout form — collects name and email, creates an Order."""
    items, total = get_cart_items(request.session)

    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect("shop:home")

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        customer_email = request.POST.get("customer_email", "").strip()

        if not customer_name or not customer_email:
            messages.error(request, "Please fill in all fields.")
            return render(
                request,
                "shop/checkout.html",
                {"cart_items": items, "cart_total": total},
            )

        # Wrap in a transaction so order + items are created together
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=customer_name,
                customer_email=customer_email,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price_at_purchase=item["product"].price,
                )
                # Reduce stock
                product = item["product"]
                product.stock_quantity -= item["quantity"]
                product.save()

            try:
                send_new_order_notification(order)
                send_order_confirmation(order)
            except Exception as exc:
                print("NEW ORDER EMAIL ERROR:", exc, flush=True)

        clear_cart(request.session)
        return redirect("shop:order_confirmation", order_id=order.pk)

    return render(
        request,
        "shop/checkout.html",
        {"cart_items": items, "cart_total": total},
    )


def order_confirmation(request, order_id):
    """Thank-you page shown after a successful checkout."""
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "shop/order_confirmation.html", {"order": order})


@login_required
def my_orders(request):
    """Show the logged-in user's order history."""
    orders = (
        Order.objects.filter(user=request.user)
        .select_related("user")
        .prefetch_related("items__product")
        .order_by("-created_at")
    )
    return render(request, "shop/my_orders.html", {"orders": orders})
