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
    helyszin    = request.args.get("helyszin", "").strip()
    tipus       = request.args.get("tipus", "").strip()
    ar_min_str  = request.args.get("ar_min", "").strip()
    ar_max_str  = request.args.get("ar_max", "").strip()
    szobak_str  = request.args.get("szobak_min", "").strip()
    emelet_str  = request.args.get("emelet", "").strip()
    terulet_str = request.args.get("terulet", "").strip()
    sort        = request.args.get("sort", "ar_asc")

    ar_min     = int(ar_min_str) if ar_min_str.isdigit() else None
    ar_max     = int(ar_max_str) if ar_max_str.isdigit() else None
    szobak_min = int(szobak_str) if szobak_str.isdigit() else None
    emelet     = int(emelet_str) if emelet_str.lstrip("-").isdigit() else None

    terulet_min = terulet_max = None
    if terulet_str == "30-40":
        terulet_min, terulet_max = 30, 40
    elif terulet_str == "40-50":
        terulet_min, terulet_max = 40, 50
    elif terulet_str == "50+":
        terulet_min = 50

    results = props.search(
        helyszin=helyszin,
        tipus=tipus,
        ar_min=ar_min,
        ar_max=ar_max,
        szobak_min=szobak_min,
        emelet=emelet,
        terulet_min=terulet_min,
        terulet_max=terulet_max,
    )

    if sort == "ar_desc":
        results = sorted(results, key=lambda p: p["ar"], reverse=True)
    elif sort == "terulet_desc":
        results = sorted(results, key=lambda p: p["terulet"], reverse=True)
    else:
        results = sorted(results, key=lambda p: p["ar"])

    active_filters = []
    base = "/ingatlan-ertekesites"

    def remove_url(*skip_keys):
        parts = []
        for k, v in [("helyszin", helyszin), ("tipus", tipus),
                     ("ar_min", ar_min_str), ("ar_max", ar_max_str),
                     ("szobak_min", szobak_str), ("emelet", emelet_str),
                     ("terulet", terulet_str), ("sort", sort)]:
            if k in skip_keys or not v:
                continue
            parts.append(f"{k}={v}")
        return base + ("?" + "&".join(parts) if parts else "")

    def fmt_m(v):
        return f"{v // 1_000_000} M Ft"

    if helyszin:
        active_filters.append((f"Helyszín: {helyszin}", remove_url("helyszin")))
    if tipus:
        active_filters.append((f"Típus: {tipus}", remove_url("tipus")))
    if ar_min or ar_max:
        if ar_min and ar_max:
            ar_label = f"{fmt_m(ar_min)} – {fmt_m(ar_max)}"
        elif ar_min:
            ar_label = f"min. {fmt_m(ar_min)}"
        else:
            ar_label = f"max. {fmt_m(ar_max)}"
        active_filters.append((ar_label, remove_url("ar_min", "ar_max")))
    if szobak_min:
        active_filters.append((f"{szobak_min} szobás", remove_url("szobak_min")))
    if emelet is not None:
        emelet_nev = "Földszint" if emelet == 0 else f"{emelet}. emelet"
        active_filters.append((emelet_nev, remove_url("emelet")))
    if terulet_str:
        terulet_nev = {"30-40": "30–40 m²", "40-50": "40–50 m²", "50+": "50 m² felett"}.get(terulet_str, terulet_str)
        active_filters.append((terulet_nev, remove_url("terulet")))

    EMELETEK = sorted(set(p["emelet"] for p in props.get_all()))

    return render_template(
        "ingatlan_ertekesites.html",
        properties=results,
        total_count=len(props.get_all()),
        tipusok=props.TIPUSOK,
        helyszinek=props.HELYSZINEK,
        emeletek=EMELETEK,
        filters={"helyszin": helyszin, "tipus": tipus,
                 "ar_min": ar_min_str, "ar_max": ar_max_str,
                 "szobak_min": szobak_str, "emelet": emelet_str, "terulet": terulet_str},
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
