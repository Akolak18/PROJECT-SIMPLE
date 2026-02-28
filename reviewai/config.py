"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///reviewai.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Anthropic / Claude
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

    # Stripe
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    # App
    APP_URL = os.environ.get("APP_URL", "http://localhost:5001")

    # Stripe Price IDs (create these in your Stripe dashboard)
    STRIPE_PRICE_STARTER = os.environ.get("STRIPE_PRICE_STARTER", "price_starter_placeholder")
    STRIPE_PRICE_GROWTH = os.environ.get("STRIPE_PRICE_GROWTH", "price_growth_placeholder")
    STRIPE_PRICE_AGENCY = os.environ.get("STRIPE_PRICE_AGENCY", "price_agency_placeholder")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
