import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import properties_data as props

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
app.jinja_env.globals["format_ar"] = props.format_ar


@app.route("/")
def index():
    return redirect(url_for("property_sales"))


@app.route("/ingatlan-ertekesites")
def property_sales():
    helyszin   = request.args.get("helyszin", "").strip()
    tipus      = request.args.get("tipus", "").strip()
    ar_max_str = request.args.get("ar_max", "").strip()
    szobak_str = request.args.get("szobak_min", "").strip()
    emelet_str = request.args.get("emelet", "").strip()
    sort       = request.args.get("sort", "ar_asc")

    ar_max     = int(ar_max_str) if ar_max_str.isdigit() else None
    szobak_min = int(szobak_str) if szobak_str.isdigit() else None
    emelet     = int(emelet_str) if emelet_str.lstrip("-").isdigit() else None

    results = props.search(
        helyszin=helyszin,
        tipus=tipus,
        ar_max=ar_max,
        szobak_min=szobak_min,
        emelet=emelet,
    )

    if sort == "ar_desc":
        results = sorted(results, key=lambda p: p["ar"], reverse=True)
    elif sort == "terulet_desc":
        results = sorted(results, key=lambda p: p["terulet"], reverse=True)
    else:
        results = sorted(results, key=lambda p: p["ar"])

    active_filters = []
    base = "/ingatlan-ertekesites"

    def remove_url(skip_key):
        parts = []
        for k, v in [("helyszin", helyszin), ("tipus", tipus),
                     ("ar_max", ar_max_str), ("szobak_min", szobak_str),
                     ("emelet", emelet_str), ("sort", sort)]:
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
    if emelet is not None:
        emelet_nev = "Földszint" if emelet == 0 else f"{emelet}. emelet"
        active_filters.append((emelet_nev, remove_url("emelet")))

    EMELETEK = sorted(set(p["emelet"] for p in props.get_all()))

    return render_template(
        "ingatlan_ertekesites.html",
        properties=results,
        total_count=len(props.get_all()),
        tipusok=props.TIPUSOK,
        helyszinek=props.HELYSZINEK,
        emeletek=EMELETEK,
        filters={"helyszin": helyszin, "tipus": tipus, "ar_max": ar_max_str,
                 "szobak_min": szobak_str, "emelet": emelet_str},
        active_filters=active_filters,
        sort=sort,
    )


@app.route("/ingatlan-ertekesites/<slug>")
def property_detail(slug):
    p = props.get_by_slug(slug)
    if p is None:
        return "Ingatlan nem található.", 404
    return render_template("ingatlan_detail.html", p=p,
                           tarolok=props.TAROLOK, parkolok=props.PARKOLOK)


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(debug=True, port=port)
