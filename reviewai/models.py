"""Database models for ReplyFast AI."""
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db


# ---------------------------------------------------------------------------
# Plans (static data — reflected in DB for easy querying)
# ---------------------------------------------------------------------------
PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "max_businesses": 1,
        "max_responses_per_month": 10,
        "features": ["1 business location", "10 AI responses/month", "Email support"],
    },
    "starter": {
        "name": "Starter",
        "price": 49,
        "max_businesses": 3,
        "max_responses_per_month": 100,
        "features": [
            "3 business locations",
            "100 AI responses/month",
            "Analytics dashboard",
            "Priority email support",
        ],
    },
    "growth": {
        "name": "Growth",
        "price": 99,
        "max_businesses": 10,
        "max_responses_per_month": -1,  # unlimited
        "features": [
            "10 business locations",
            "Unlimited AI responses",
            "Advanced analytics",
            "Custom brand voice",
            "Chat support",
        ],
    },
    "agency": {
        "name": "Agency",
        "price": 249,
        "max_businesses": -1,  # unlimited
        "max_responses_per_month": -1,
        "features": [
            "Unlimited locations",
            "Unlimited AI responses",
            "White-label portal",
            "API access",
            "Dedicated account manager",
        ],
    },
}


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    plan = db.Column(db.String(50), default="free", nullable=False)
    stripe_customer_id = db.Column(db.String(255), unique=True, nullable=True)
    stripe_subscription_id = db.Column(db.String(255), unique=True, nullable=True)
    subscription_status = db.Column(db.String(50), default="inactive")
    current_period_end = db.Column(db.DateTime, nullable=True)
    brand_voice = db.Column(db.Text, nullable=True)  # custom AI instructions
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    businesses = db.relationship("Business", back_populates="owner", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def plan_info(self) -> dict:
        return PLANS.get(self.plan, PLANS["free"])

    @property
    def responses_used_this_month(self) -> int:
        now = datetime.now(timezone.utc)
        return (
            Review.query.join(Business)
            .filter(
                Business.user_id == self.id,
                Review.responded == True,
                db.extract("month", Review.responded_at) == now.month,
                db.extract("year", Review.responded_at) == now.year,
            )
            .count()
        )

    @property
    def can_generate_response(self) -> bool:
        info = self.plan_info
        limit = info["max_responses_per_month"]
        if limit == -1:
            return True
        return self.responses_used_this_month < limit

    @property
    def business_count(self) -> int:
        return Business.query.filter_by(user_id=self.id).count()

    @property
    def can_add_business(self) -> bool:
        limit = self.plan_info["max_businesses"]
        if limit == -1:
            return True
        return self.business_count < limit


class Business(db.Model):
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=True)  # restaurant, salon, gym, …
    address = db.Column(db.String(500), nullable=True)
    google_place_id = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(500), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    owner = db.relationship("User", back_populates="businesses")
    reviews = db.relationship("Review", back_populates="business", cascade="all, delete-orphan")

    @property
    def avg_rating(self):
        ratings = [r.rating for r in self.reviews]
        return round(sum(ratings) / len(ratings), 1) if ratings else 0.0

    @property
    def response_rate(self):
        total = len(self.reviews)
        if total == 0:
            return 0
        responded = sum(1 for r in self.reviews if r.responded)
        return round((responded / total) * 100)

    @property
    def pending_reviews(self):
        return [r for r in self.reviews if not r.responded]


class Review(db.Model):
    __tablename__ = "reviews"

    PLATFORMS = ["google", "yelp", "facebook", "tripadvisor", "other"]

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False, index=True)
    platform = db.Column(db.String(50), default="google", nullable=False)
    reviewer_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    content = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.Date, nullable=True)
    responded = db.Column(db.Boolean, default=False)
    response_text = db.Column(db.Text, nullable=True)
    ai_generated = db.Column(db.Boolean, default=False)
    responded_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    business = db.relationship("Business", back_populates="reviews")

    @property
    def sentiment(self):
        if self.rating >= 4:
            return "positive"
        elif self.rating == 3:
            return "neutral"
        return "negative"

    @property
    def stars(self):
        return "★" * self.rating + "☆" * (5 - self.rating)
