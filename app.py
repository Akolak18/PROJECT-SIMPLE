"""
Reservation export app for cleaners.

Run:
    cp .env.example .env          # fill in credentials
    pip install -r requirements.txt
    python app.py
Then open http://localhost:5000
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, Response

import previo_client as previo
from excel_export import build_excel

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")


@app.route("/ingatlan-ertekesites")
def property_sales():
    return render_template("property_sales.html")


@app.route("/")
def index():
    today = datetime.today()
    date_from = request.args.get("date_from", today.strftime("%Y-%m-%d"))
    date_to   = request.args.get("date_to",   (today + timedelta(days=30)).strftime("%Y-%m-%d"))
    refresh   = int(os.environ.get("REFRESH_INTERVAL", 60))
    return render_template("index.html", date_from=date_from, date_to=date_to, refresh_interval=refresh)


@app.route("/api/reservations")
def api_reservations():
    """JSON endpoint — polled by the frontend for live data."""
    today = datetime.today()
    date_from = request.args.get("date_from", today.strftime("%Y-%m-%d"))
    date_to   = request.args.get("date_to",   (today + timedelta(days=30)).strftime("%Y-%m-%d"))

    try:
        raw  = previo.get_reservations(date_from, date_to)
        rows = previo.flatten_reservations(raw)
        return jsonify({"ok": True, "rows": rows, "count": len(rows)})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/export/excel")
def export_excel():
    """Download an Excel file for the selected date range."""
    today = datetime.today()
    date_from = request.args.get("date_from", today.strftime("%Y-%m-%d"))
    date_to   = request.args.get("date_to",   (today + timedelta(days=30)).strftime("%Y-%m-%d"))

    try:
        raw  = previo.get_reservations(date_from, date_to)
        rows = previo.flatten_reservations(raw)
        xlsx = build_excel(rows, date_from, date_to)
    except Exception as exc:
        return f"Error generating Excel: {exc}", 500

    filename = f"cleaning_schedule_{date_from}_{date_to}.xlsx"
    return Response(
        xlsx,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
