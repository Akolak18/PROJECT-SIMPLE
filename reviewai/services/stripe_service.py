"""Stripe billing integration."""
from __future__ import annotations
import os

try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False


def _init():
    if STRIPE_AVAILABLE:
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")


_init()

PLAN_PRICE_MAP = {
    "starter": os.environ.get("STRIPE_PRICE_STARTER", ""),
    "growth": os.environ.get("STRIPE_PRICE_GROWTH", ""),
    "agency": os.environ.get("STRIPE_PRICE_AGENCY", ""),
}


def create_customer(email: str, name: str) -> str | None:
    """Create a Stripe customer and return the customer ID."""
    if not STRIPE_AVAILABLE or not stripe.api_key:
        return None
    try:
        customer = stripe.Customer.create(email=email, name=name)
        return customer.id
    except Exception:
        return None


def create_checkout_session(
    customer_id: str,
    plan: str,
    success_url: str,
    cancel_url: str,
) -> str | None:
    """Create a Stripe Checkout session and return the session URL."""
    if not STRIPE_AVAILABLE or not stripe.api_key:
        return None
    price_id = PLAN_PRICE_MAP.get(plan)
    if not price_id:
        return None
    try:
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url
    except Exception:
        return None


def create_portal_session(customer_id: str, return_url: str) -> str | None:
    """Create a Stripe Customer Portal session."""
    if not STRIPE_AVAILABLE or not stripe.api_key:
        return None
    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        return session.url
    except Exception:
        return None


def construct_webhook_event(payload: bytes, sig_header: str):
    """Parse and verify an incoming Stripe webhook."""
    if not STRIPE_AVAILABLE:
        return None
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    try:
        return stripe.Webhook.construct_event(payload, sig_header, secret)
    except Exception:
        return None
