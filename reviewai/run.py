"""Entry point — run with: python run.py"""
import os
from app import create_app

env = os.environ.get("FLASK_ENV", "development")
application = create_app(env)

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5001))
    application.run(debug=(env == "development"), port=port)
