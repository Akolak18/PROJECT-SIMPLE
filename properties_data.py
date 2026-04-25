PROPERTIES = [
    {
        "id": 1,
        "slug": "budapest-viii-rakoczi-ut-lakas",
        "cim": "Rákóczi út 12.",
        "helyszin": "Budapest",
        "kerulet": "VIII. kerület",
        "teljes_cim": "Budapest, VIII. kerület – Rákóczi út 12.",
        "tipus": "Lakás",
        "ar": 0,
        "terulet": 0,
        "szobak": 0,
        "furdoszoba": 1,
        "emelet": 2,
        "epitesi_ev": 2010,
        "allapot": "Újszerű",
        "leiras": "Eladó lakás Budapest VIII. kerületében, a Rákóczi úton. Részletek hamarosan.",
        "kepek": [
            "/static/images/utcafront.png",
            "/static/images/utcafront2.png",
        ],
        "szolgaltatasok": ["Lift", "Erkély", "Klíma"],
        "cimke": "",
        "energiaosztaly": "C",
    },
    {
        "id": 2,
        "slug": "budapest-viii-baross-utca-lakas",
        "cim": "Baross utca 34.",
        "helyszin": "Budapest",
        "kerulet": "VIII. kerület",
        "teljes_cim": "Budapest, VIII. kerület – Baross utca 34.",
        "tipus": "Lakás",
        "ar": 0,
        "terulet": 0,
        "szobak": 0,
        "furdoszoba": 1,
        "emelet": 3,
        "epitesi_ev": 2015,
        "allapot": "Újszerű",
        "leiras": "Eladó lakás Budapest VIII. kerületében, a Baross utcán. Részletek hamarosan.",
        "kepek": [
            "/static/images/utcafront2.png",
            "/static/images/utcafront3.png",
        ],
        "szolgaltatasok": ["Lift", "Klíma", "Beépített konyha"],
        "cimke": "",
        "energiaosztaly": "B",
    },
    {
        "id": 3,
        "slug": "budapest-viii-ulloi-ut-lakas",
        "cim": "Üllői út 56.",
        "helyszin": "Budapest",
        "kerulet": "VIII. kerület",
        "teljes_cim": "Budapest, VIII. kerület – Üllői út 56.",
        "tipus": "Lakás",
        "ar": 0,
        "terulet": 0,
        "szobak": 0,
        "furdoszoba": 1,
        "emelet": 1,
        "epitesi_ev": 2018,
        "allapot": "Új építésű",
        "leiras": "Eladó lakás Budapest VIII. kerületében, az Üllői úton. Részletek hamarosan.",
        "kepek": [
            "/static/images/utcafront3.png",
            "/static/images/utcafront4.png",
        ],
        "szolgaltatasok": ["Lift", "Erkély", "Garázs"],
        "cimke": "Új",
        "energiaosztaly": "A",
    },
    {
        "id": 4,
        "slug": "budapest-viii-krudy-utca-lakas",
        "cim": "Krúdy Gyula utca 8.",
        "helyszin": "Budapest",
        "kerulet": "VIII. kerület",
        "teljes_cim": "Budapest, VIII. kerület – Krúdy Gyula utca 8.",
        "tipus": "Lakás",
        "ar": 0,
        "terulet": 0,
        "szobak": 0,
        "furdoszoba": 1,
        "emelet": 4,
        "epitesi_ev": 2020,
        "allapot": "Új építésű",
        "leiras": "Eladó lakás Budapest VIII. kerületében, a Krúdy Gyula utcán. Részletek hamarosan.",
        "kepek": [
            "/static/images/utcafront4.png",
        ],
        "szolgaltatasok": ["Lift", "Klíma", "Erkély", "Beépített szekrények"],
        "cimke": "Kiemelt",
        "energiaosztaly": "A+",
    },
    {
        "id": 5,
        "slug": "budapest-viii-mikszath-ter-lakas",
        "cim": "Mikszáth Kálmán tér 3.",
        "helyszin": "Budapest",
        "kerulet": "VIII. kerület",
        "teljes_cim": "Budapest, VIII. kerület – Mikszáth Kálmán tér 3.",
        "tipus": "Lakás",
        "ar": 0,
        "terulet": 0,
        "szobak": 0,
        "furdoszoba": 2,
        "emelet": 2,
        "epitesi_ev": 2019,
        "allapot": "Újszerű",
        "leiras": "Eladó lakás Budapest VIII. kerületében, a Mikszáth Kálmán téren. Részletek hamarosan.",
        "kepek": [
            "/static/images/utcafront.png",
            "/static/images/Belsőudvar.png",
        ],
        "szolgaltatasok": ["Lift", "2 fürdőszoba", "Erkély", "Klíma", "Garázs"],
        "cimke": "Prémium",
        "energiaosztaly": "B",
    },
    {
        "id": 6,
        "slug": "budapest-viii-jozsef-korut-lakas",
        "cim": "József körút 21.",
        "helyszin": "Budapest",
        "kerulet": "VIII. kerület",
        "teljes_cim": "Budapest, VIII. kerület – József körút 21.",
        "tipus": "Lakás",
        "ar": 0,
        "terulet": 0,
        "szobak": 0,
        "furdoszoba": 1,
        "emelet": 3,
        "epitesi_ev": 2016,
        "allapot": "Felújított",
        "leiras": "Eladó lakás Budapest VIII. kerületében, a József körúton. Részletek hamarosan.",
        "kepek": [
            "/static/images/Belsőudvar.png",
            "/static/images/utcafront3.png",
        ],
        "szolgaltatasok": ["Lift", "Erkély", "Klíma"],
        "cimke": "",
        "energiaosztaly": "C",
    },
]

CONTACT_PHONE = "+36 1 111 1111"
CONTACT_EMAIL = "gueswhat@gmail.com"


def get_all():
    return PROPERTIES


def get_by_id(property_id):
    return next((p for p in PROPERTIES if p["id"] == property_id), None)


def get_by_slug(slug):
    return next((p for p in PROPERTIES if p["slug"] == slug), None)


def search(helyszin="", tipus="", ar_min=None, ar_max=None, szobak_min=None):
    results = [p for p in PROPERTIES if p["ar"] > 0 or True]
    if helyszin:
        h = helyszin.lower()
        results = [p for p in results if h in p["helyszin"].lower() or h in p["kerulet"].lower()]
    if tipus:
        results = [p for p in results if p["tipus"] == tipus]
    if ar_max is not None:
        results = [p for p in results if p["ar"] == 0 or p["ar"] <= ar_max]
    if szobak_min is not None:
        results = [p for p in results if p["szobak"] == 0 or p["szobak"] >= szobak_min]
    return results


def format_ar(ar):
    if ar == 0:
        return "Ár hamarosan"
    if ar >= 1_000_000:
        m = ar / 1_000_000
        if m == int(m):
            return f"{int(m)} M Ft"
        return f"{m:.1f} M Ft"
    return f"{ar:,} Ft".replace(",", " ")


HELYSZINEK = sorted(set(p["helyszin"] for p in PROPERTIES))
TIPUSOK = sorted(set(p["tipus"] for p in PROPERTIES))
