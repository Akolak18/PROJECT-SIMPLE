"""
Iza-Szondi Homes — web app.

Public website:  http://localhost:5000/
Booking form:    http://localhost:5000/#book  (POST → /book)
Admin schedule:  http://localhost:5000/admin
Admin bookings:  http://localhost:5000/admin/bookings

Run:
    cp .env.example .env          # fill in credentials
    pip install -r requirements.txt
    python app.py
"""

import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, Response, url_for

import previo_client as previo
from excel_export import build_excel

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

DATABASE = Path(__file__).parent / "bookings.db"


# ── Database helpers ──────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT NOT NULL,
                email     TEXT NOT NULL,
                phone     TEXT,
                check_in  TEXT NOT NULL,
                check_out TEXT NOT NULL,
                guests    INTEGER,
                room_pref TEXT,
                message   TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                status    TEXT DEFAULT 'new'
            )
        """)
        conn.commit()


init_db()


# ── Public website ────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("home.html", booking_success=False)


@app.route("/book", methods=["POST"])
def book():
    name      = request.form.get("name", "").strip()
    email     = request.form.get("email", "").strip()
    phone     = request.form.get("phone", "").strip()
    check_in  = request.form.get("check_in", "").strip()
    check_out = request.form.get("check_out", "").strip()
    guests    = request.form.get("guests", "").strip()
    room_pref = request.form.get("room_pref", "").strip()
    message   = request.form.get("message", "").strip()

    if not (name and email and check_in and check_out):
        return render_template("home.html", booking_success=False), 400

    with get_db() as conn:
        conn.execute(
            "INSERT INTO bookings (name, email, phone, check_in, check_out, guests, room_pref, message)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, email, phone or None, check_in, check_out,
             int(guests) if guests.isdigit() else None,
             room_pref or None, message or None)
        )
        conn.commit()

    return render_template("home.html", booking_success=True)


# ── Admin — cleaning schedule ─────────────────────────────────────────────────

@app.route("/admin")
def admin():
    today     = datetime.today()
    date_from = request.args.get("date_from", today.strftime("%Y-%m-%d"))
    date_to   = request.args.get("date_to",   (today + timedelta(days=30)).strftime("%Y-%m-%d"))
    refresh   = int(os.environ.get("REFRESH_INTERVAL", 60))
    return render_template("index.html", date_from=date_from, date_to=date_to, refresh_interval=refresh)


@app.route("/api/reservations")
def api_reservations():
    """JSON endpoint — polled by the frontend for live data."""
    today     = datetime.today()
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
    today     = datetime.today()
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


# ── Admin — booking requests ──────────────────────────────────────────────────

@app.route("/admin/bookings")
def admin_bookings():
    with get_db() as conn:
        bookings = conn.execute(
            "SELECT * FROM bookings ORDER BY created_at DESC"
        ).fetchall()
    return render_template("admin_bookings.html", bookings=bookings)


@app.route("/admin/bookings/<int:booking_id>/status", methods=["POST"])
def update_booking_status(booking_id):
    status = request.form.get("status", "new")
    if status not in ("new", "confirmed", "cancelled"):
        status = "new"
    with get_db() as conn:
        conn.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
        conn.commit()
    return redirect(url_for("admin_bookings"))


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
