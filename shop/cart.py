"""
Session-based shopping cart helpers.

The cart is stored in the user's browser session (no login required).
Structure: {"product_id": {"quantity": 2}, ...}
"""

from decimal import Decimal

from .models import Product

CART_SESSION_KEY = "cart"


def get_cart(session):
    """Return the raw cart dict from the session."""
    return session.get(CART_SESSION_KEY, {})


def save_cart(session, cart):
    """Persist cart changes back to the session."""
    session[CART_SESSION_KEY] = cart
    session.modified = True


def add_to_cart(session, product_id, quantity=1):
    """Add a product to the cart (or increase its quantity)."""
    cart = get_cart(session)
    key = str(product_id)
    if key in cart:
        cart[key]["quantity"] += quantity
    else:
        cart[key] = {"quantity": quantity}
    save_cart(session, cart)


def update_cart_item(session, product_id, quantity):
    """Set the quantity for a cart item. Removes it if quantity is 0."""
    cart = get_cart(session)
    key = str(product_id)
    if quantity <= 0:
        cart.pop(key, None)
    elif key in cart:
        cart[key]["quantity"] = quantity
    save_cart(session, cart)


def remove_from_cart(session, product_id):
    """Remove a product entirely from the cart."""
    cart = get_cart(session)
    cart.pop(str(product_id), None)
    save_cart(session, cart)


def clear_cart(session):
    """Empty the cart (called after a successful checkout)."""
    if CART_SESSION_KEY in session:
        del session[CART_SESSION_KEY]
        session.modified = True


def cart_item_count(session):
    """Total number of items in the cart (for the navbar badge)."""
    cart = get_cart(session)
    return sum(item["quantity"] for item in cart.values())


def get_cart_items(session):
    """
    Build a list of cart line items with product details and subtotals.
    Returns (items_list, total) where each item is a dict with
    product, quantity, and subtotal keys.
    """
    cart = get_cart(session)
    items = []
    total = Decimal("0.00")

    for product_id, data in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            continue

        quantity = data["quantity"]
        subtotal = product.price * quantity
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )
        total += subtotal

    return items, total
