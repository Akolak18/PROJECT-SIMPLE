"""Stripe billing blueprint — plans, checkout, webhooks, portal."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user

from extensions import db
from models import PLANS
from services import stripe_service

bp = Blueprint("billing", __name__, url_prefix="/billing")


@bp.route("/plans")
@login_required
def plans():
    return render_template("billing/plans.html", plans=PLANS, current_plan=current_user.plan)


@bp.route("/subscribe/<plan>", methods=["POST"])
@login_required
def subscribe(plan: str):
    if plan not in ("starter", "growth", "agency"):
        flash("Invalid plan.", "error")
        return redirect(url_for("billing.plans"))

    if not current_user.stripe_customer_id:
        flash("Billing setup incomplete. Please contact support.", "error")
        return redirect(url_for("billing.plans"))

    session_url = stripe_service.create_checkout_session(
        customer_id=current_user.stripe_customer_id,
        plan=plan,
        success_url=url_for("billing.success", _external=True) + f"?plan={plan}",
        cancel_url=url_for("billing.plans", _external=True),
    )

    if not session_url:
        flash("Stripe is not configured. Set STRIPE_SECRET_KEY and STRIPE_PRICE_* env vars.", "error")
        return redirect(url_for("billing.plans"))

    return redirect(session_url)


@bp.route("/success")
@login_required
def success():
    plan = request.args.get("plan", "starter")
    flash(f"You're now on the {plan.title()} plan! Enjoy unlimited reviews.", "success")
    return redirect(url_for("dashboard.index"))


@bp.route("/portal", methods=["POST"])
@login_required
def portal():
    if not current_user.stripe_customer_id:
        flash("No billing account found.", "error")
        return redirect(url_for("dashboard.settings"))

    portal_url = stripe_service.create_portal_session(
        customer_id=current_user.stripe_customer_id,
        return_url=url_for("dashboard.settings", _external=True),
    )

    if not portal_url:
        flash("Stripe portal is not configured.", "error")
        return redirect(url_for("dashboard.settings"))

    return redirect(portal_url)


@bp.route("/webhook", methods=["POST"])
def webhook():
    """Handle Stripe webhook events."""
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature", "")

    event = stripe_service.construct_webhook_event(payload, sig_header)
    if event is None:
        return "Webhook error", 400

    if event["type"] == "customer.subscription.updated":
        _handle_subscription_update(event["data"]["object"])
    elif event["type"] == "customer.subscription.deleted":
        _handle_subscription_deleted(event["data"]["object"])

    return "OK", 200


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------
def _handle_subscription_update(subscription):
    from models import User
    from datetime import datetime, timezone

    user = User.query.filter_by(stripe_customer_id=subscription["customer"]).first()
    if not user:
        return

    # Map Stripe price ID → plan name
    price_id = subscription["items"]["data"][0]["price"]["id"]
    price_plan_map = {
        current_app.config["STRIPE_PRICE_STARTER"]: "starter",
        current_app.config["STRIPE_PRICE_GROWTH"]: "growth",
        current_app.config["STRIPE_PRICE_AGENCY"]: "agency",
    }
    new_plan = price_plan_map.get(price_id, "free")

    user.plan = new_plan
    user.stripe_subscription_id = subscription["id"]
    user.subscription_status = subscription["status"]
    period_end = subscription.get("current_period_end")
    if period_end:
        user.current_period_end = datetime.fromtimestamp(period_end, tz=timezone.utc)
    db.session.commit()


def _handle_subscription_deleted(subscription):
    from models import User

    user = User.query.filter_by(stripe_customer_id=subscription["customer"]).first()
    if not user:
        return
    user.plan = "free"
    user.subscription_status = "cancelled"
    db.session.commit()
