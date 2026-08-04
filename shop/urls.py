"""
URL routes for the shop app — maps URL paths to view functions.
"""

from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        views.ShopLoginView.as_view(),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "order/<int:order_id>/confirmation/",
        views.order_confirmation,
        name="order_confirmation",
    ),
]
