"""Landing page and public routes."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from models import PLANS

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return render_template("landing.html", plans=PLANS)


@bp.route("/pricing")
def pricing():
    return render_template("pricing.html", plans=PLANS)
