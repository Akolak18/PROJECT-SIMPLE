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
from flask import Flask, jsonify, render_template, request, Response, redirect, url_for

import previo_client as previo
from excel_export import build_excel
import properties_data as props

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

app.jinja_env.globals["format_ar"] = props.format_ar


@app.route("/")
def index():
    return redirect(url_for("property_sales"))


@app.route("/takarito")
def cleaning_schedule():
    today = datetime.today()
    date_from = request.args.get("date_from", today.strftime("%Y-%m-%d"))
    date_to   = request.args.get("date_to",   (today + timedelta(days=30)).strftime("%Y-%m-%d"))
    refresh   = int(os.environ.get("REFRESH_INTERVAL", 60))
    return render_template("index.html", date_from=date_from, date_to=date_to, refresh_interval=refresh)


@app.route("/ingatlan-ertekesites")
def property_sales():
    helyszin   = request.args.get("helyszin", "").strip()
    tipus      = request.args.get("tipus", "").strip()
    ar_max_str = request.args.get("ar_max", "").strip()
    szobak_str = request.args.get("szobak_min", "").strip()
    sort       = request.args.get("sort", "ar_asc")

    ar_max    = int(ar_max_str)    if ar_max_str.isdigit()    else None
    szobak_min = int(szobak_str)   if szobak_str.isdigit()    else None

    results = props.search(
        helyszin=helyszin,
        tipus=tipus,
        ar_max=ar_max,
        szobak_min=szobak_min,
    )

    if sort == "ar_desc":
        results = sorted(results, key=lambda p: p["ar"], reverse=True)
    elif sort == "terulet_desc":
        results = sorted(results, key=lambda p: p["terulet"], reverse=True)
    else:
        results = sorted(results, key=lambda p: p["ar"])

    # Build active filter tags with remove-links
    active_filters = []
    base = "/ingatlan-ertekesites"

    def remove_url(skip_key):
        parts = []
        for k, v in [("helyszin", helyszin), ("tipus", tipus),
                     ("ar_max", ar_max_str), ("szobak_min", szobak_str), ("sort", sort)]:
            if k == skip_key or not v:
                continue
            parts.append(f"{k}={v}")
        return base + ("?" + "&".join(parts) if parts else "")

    if helyszin:
        active_filters.append((f"Helyszín: {helyszin}", remove_url("helyszin")))
    if tipus:
        active_filters.append((f"Típus: {tipus}", remove_url("tipus")))
    if ar_max:
        active_filters.append((f"Max. ár: {props.format_ar(ar_max)}", remove_url("ar_max")))
    if szobak_min:
        active_filters.append((f"{szobak_min}+ szoba", remove_url("szobak_min")))

    return render_template(
        "ingatlan_ertekesites.html",
        properties=results,
        total_count=len(props.get_all()),
        tipusok=props.TIPUSOK,
        helyszinek=props.HELYSZINEK,
        filters={"helyszin": helyszin, "tipus": tipus, "ar_max": ar_max_str, "szobak_min": szobak_str},
        active_filters=active_filters,
        sort=sort,
    )


@app.route("/ingatlan-ertekesites/<slug>")
def property_detail(slug):
    p = props.get_by_slug(slug)
    if p is None:
        return "Ingatlan nem található.", 404
    return render_template("ingatlan_detail.html", p=p)


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
