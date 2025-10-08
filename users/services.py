import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_name):
    """Создает продукт в stripe."""

    product = stripe.Product.create(name=product_name)
    return product.get("id")


def create_stripe_price(amount):
    """Создает цену в stripe."""

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": "Payment"},
    )


def create_stripe_sessions(price):
    """Создает сессию на оплату в stripe."""

    session = stripe.checkout.Session.create(
        success_url="https://localhost:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("url"), session.get("payment_method_types")
