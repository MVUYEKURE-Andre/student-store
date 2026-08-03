"""
Management command to seed the database with 10 sample products.

Usage: python manage.py seed_products
"""

from decimal import Decimal

from django.core.management.base import BaseCommand

from shop.models import Product

SAMPLE_PRODUCTS = [
    {
        "name": "Wireless Earbuds",
        "description": "Compact Bluetooth earbuds with 24-hour battery life. Perfect for studying on the go.",
        "price": Decimal("29.99"),
        "image_url": "https://picsum.photos/seed/earbuds/400/400",
        "stock_quantity": 50,
    },
    {
        "name": "Laptop Stand",
        "description": "Adjustable aluminum laptop stand to improve posture during long study sessions.",
        "price": Decimal("34.99"),
        "image_url": "https://picsum.photos/seed/laptop-stand/400/400",
        "stock_quantity": 30,
    },
    {
        "name": "Notebook Set (3-pack)",
        "description": "Three ruled A5 notebooks with thick paper — ideal for lecture notes.",
        "price": Decimal("12.99"),
        "image_url": "https://picsum.photos/seed/notebook-set/400/400",
        "stock_quantity": 100,
    },
    {
        "name": "Insulated Water Bottle",
        "description": "32 oz stainless steel bottle keeps drinks cold for 24 hours.",
        "price": Decimal("19.99"),
        "image_url": "https://picsum.photos/seed/water-bottle/400/400",
        "stock_quantity": 75,
    },
    {
        "name": "Desk Lamp",
        "description": "LED desk lamp with three brightness levels and a flexible gooseneck.",
        "price": Decimal("24.99"),
        "image_url": "https://picsum.photos/seed/desk-lamp/400/400",
        "stock_quantity": 40,
    },
    {
        "name": "Backpack",
        "description": "Durable 25L backpack with padded laptop sleeve and water-resistant fabric.",
        "price": Decimal("49.99"),
        "image_url": "https://picsum.photos/seed/backpack/400/400",
        "stock_quantity": 25,
    },
    {
        "name": "Mechanical Keyboard",
        "description": "Compact 60% mechanical keyboard with blue switches — great for coding.",
        "price": Decimal("59.99"),
        "image_url": "https://picsum.photos/seed/mechanical-keyboard/400/400",
        "stock_quantity": 20,
    },
    {
        "name": "Sticky Notes (6-pack)",
        "description": "Assorted color sticky notes for reminders, flashcards, and planning.",
        "price": Decimal("8.99"),
        "image_url": "https://picsum.photos/seed/sticky-notes/400/400",
        "stock_quantity": 120,
    },
    {
        "name": "USB-C Hub",
        "description": "7-in-1 USB-C hub with HDMI, SD card reader, and 3 USB ports.",
        "price": Decimal("39.99"),
        "image_url": "https://picsum.photos/seed/usb-c-hub/400/400",
        "stock_quantity": 35,
    },
    {
        "name": "Coffee Mug",
        "description": "Ceramic mug with 'Powered by Coffee' print — holds 12 oz.",
        "price": Decimal("14.99"),
        "image_url": "https://picsum.photos/seed/coffee-mug/400/400",
        "stock_quantity": 60,
    },
]


class Command(BaseCommand):
    help = "Seed the database with 10 sample products for testing"

    def handle(self, *args, **options):
        Product.objects.all().delete()

        created_count = 0
        for data in SAMPLE_PRODUCTS:
            Product.objects.create(**data)
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Replaced existing products and created {created_count} sample items."
            )
        )
