"""Authentication blueprint — register, login, logout."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User
from services.stripe_service import create_customer

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = []
        if not full_name:
            errors.append("Full name is required.")
        if not email or "@" not in email:
            errors.append("A valid email address is required.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if User.query.filter_by(email=email).first():
            errors.append("An account with that email already exists.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("auth/register.html", full_name=full_name, email=email)

        user = User(full_name=full_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # get id before commit

        # Create Stripe customer in background (non-blocking)
        stripe_id = create_customer(email, full_name)
        if stripe_id:
            user.stripe_customer_id = stripe_id

        db.session.commit()
        login_user(user)
        flash("Welcome to ReplyFast AI! Your free account is ready.", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return render_template("auth/login.html", email=email)

        login_user(user, remember=remember)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.index"))
