"""
Template context processors — inject data into every template automatically.

cart_count is used by base.html to show the cart badge in the navbar.
"""

from .cart import cart_item_count


def cart_count(request):
    """Add cart_item_count to every template context."""
    return {"cart_item_count": cart_item_count(request.session)}
