"""Dashboard blueprint — businesses, reviews, settings."""
from __future__ import annotations
from datetime import date, datetime, timezone

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from extensions import db
from models import Business, Review, PLANS
from services.ai_service import generate_response

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# ---------------------------------------------------------------------------
# Dashboard home
# ---------------------------------------------------------------------------
@bp.route("/")
@login_required
def index():
    businesses = Business.query.filter_by(user_id=current_user.id).all()
    total_reviews = sum(len(b.reviews) for b in businesses)
    pending = sum(len(b.pending_reviews) for b in businesses)
    responded = total_reviews - pending
    avg_rating = 0.0
    if total_reviews:
        all_ratings = [r.rating for b in businesses for r in b.reviews]
        avg_rating = round(sum(all_ratings) / len(all_ratings), 1)

    recent_reviews = (
        Review.query.join(Business)
        .filter(Business.user_id == current_user.id)
        .order_by(Review.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        businesses=businesses,
        total_reviews=total_reviews,
        pending=pending,
        responded=responded,
        avg_rating=avg_rating,
        recent_reviews=recent_reviews,
        plan=current_user.plan_info,
        responses_used=current_user.responses_used_this_month,
    )


# ---------------------------------------------------------------------------
# Businesses
# ---------------------------------------------------------------------------
@bp.route("/businesses")
@login_required
def businesses():
    biz_list = Business.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard/businesses.html", businesses=biz_list)


@bp.route("/businesses/add", methods=["POST"])
@login_required
def add_business():
    if not current_user.can_add_business:
        flash("You've reached the business limit for your plan. Please upgrade.", "error")
        return redirect(url_for("dashboard.businesses"))

    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    address = request.form.get("address", "").strip()
    website = request.form.get("website", "").strip()
    phone = request.form.get("phone", "").strip()

    if not name:
        flash("Business name is required.", "error")
        return redirect(url_for("dashboard.businesses"))

    biz = Business(
        user_id=current_user.id,
        name=name,
        category=category or None,
        address=address or None,
        website=website or None,
        phone=phone or None,
    )
    db.session.add(biz)
    db.session.commit()
    flash(f'"{name}" has been added successfully.', "success")
    return redirect(url_for("dashboard.businesses"))


@bp.route("/businesses/<int:biz_id>/delete", methods=["POST"])
@login_required
def delete_business(biz_id: int):
    biz = Business.query.filter_by(id=biz_id, user_id=current_user.id).first_or_404()
    name = biz.name
    db.session.delete(biz)
    db.session.commit()
    flash(f'"{name}" and all its reviews have been deleted.', "info")
    return redirect(url_for("dashboard.businesses"))


# ---------------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------------
@bp.route("/reviews")
@login_required
def reviews():
    biz_id = request.args.get("business_id", type=int)
    platform = request.args.get("platform")
    status = request.args.get("status")  # pending | responded

    query = Review.query.join(Business).filter(Business.user_id == current_user.id)

    if biz_id:
        query = query.filter(Review.business_id == biz_id)
    if platform:
        query = query.filter(Review.platform == platform)
    if status == "pending":
        query = query.filter(Review.responded == False)
    elif status == "responded":
        query = query.filter(Review.responded == True)

    review_list = query.order_by(Review.created_at.desc()).all()
    businesses = Business.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "dashboard/reviews.html",
        reviews=review_list,
        businesses=businesses,
        selected_biz=biz_id,
        selected_platform=platform,
        selected_status=status,
        platforms=Review.PLATFORMS,
    )


@bp.route("/reviews/add", methods=["POST"])
@login_required
def add_review():
    biz_id = request.form.get("business_id", type=int)
    biz = Business.query.filter_by(id=biz_id, user_id=current_user.id).first()
    if not biz:
        flash("Business not found.", "error")
        return redirect(url_for("dashboard.reviews"))

    reviewer_name = request.form.get("reviewer_name", "").strip()
    rating = request.form.get("rating", type=int)
    content = request.form.get("content", "").strip()
    platform = request.form.get("platform", "google")
    review_date_str = request.form.get("review_date", "")

    if not reviewer_name or not rating:
        flash("Reviewer name and rating are required.", "error")
        return redirect(url_for("dashboard.reviews"))

    review_date = None
    if review_date_str:
        try:
            review_date = date.fromisoformat(review_date_str)
        except ValueError:
            pass

    review = Review(
        business_id=biz_id,
        reviewer_name=reviewer_name,
        rating=rating,
        content=content or None,
        platform=platform,
        review_date=review_date or date.today(),
    )
    db.session.add(review)
    db.session.commit()
    flash("Review added. Click 'Generate AI Response' to create a reply.", "success")
    return redirect(url_for("dashboard.reviews"))


@bp.route("/reviews/<int:review_id>/generate", methods=["POST"])
@login_required
def generate_review_response(review_id: int):
    review = Review.query.join(Business).filter(
        Review.id == review_id,
        Business.user_id == current_user.id,
    ).first_or_404()

    if not current_user.can_generate_response:
        return jsonify({"ok": False, "error": "Monthly response limit reached. Please upgrade your plan."}), 403

    response_text = generate_response(
        business_name=review.business.name,
        business_category=review.business.category,
        reviewer_name=review.reviewer_name,
        rating=review.rating,
        review_text=review.content,
        brand_voice=current_user.brand_voice,
    )

    return jsonify({"ok": True, "response": response_text})


@bp.route("/reviews/<int:review_id>/respond", methods=["POST"])
@login_required
def save_response(review_id: int):
    review = Review.query.join(Business).filter(
        Review.id == review_id,
        Business.user_id == current_user.id,
    ).first_or_404()

    response_text = request.form.get("response_text", "").strip()
    ai_generated = request.form.get("ai_generated") == "true"

    if not response_text:
        flash("Response text cannot be empty.", "error")
        return redirect(url_for("dashboard.reviews"))

    review.response_text = response_text
    review.responded = True
    review.ai_generated = ai_generated
    review.responded_at = datetime.now(timezone.utc)
    db.session.commit()
    flash("Response saved successfully.", "success")
    return redirect(url_for("dashboard.reviews"))


@bp.route("/reviews/<int:review_id>/unreply", methods=["POST"])
@login_required
def unreply(review_id: int):
    review = Review.query.join(Business).filter(
        Review.id == review_id,
        Business.user_id == current_user.id,
    ).first_or_404()
    review.responded = False
    review.response_text = None
    review.responded_at = None
    db.session.commit()
    return redirect(url_for("dashboard.reviews"))


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "profile":
            current_user.full_name = request.form.get("full_name", "").strip() or current_user.full_name
            db.session.commit()
            flash("Profile updated.", "success")

        elif action == "brand_voice":
            current_user.brand_voice = request.form.get("brand_voice", "").strip() or None
            db.session.commit()
            flash("Brand voice saved. AI will use this for future responses.", "success")

        elif action == "password":
            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")
            confirm = request.form.get("confirm_password", "")
            if not current_user.check_password(current_password):
                flash("Current password is incorrect.", "error")
            elif len(new_password) < 8:
                flash("New password must be at least 8 characters.", "error")
            elif new_password != confirm:
                flash("Passwords do not match.", "error")
            else:
                current_user.set_password(new_password)
                db.session.commit()
                flash("Password changed successfully.", "success")

    return render_template("dashboard/settings.html")
