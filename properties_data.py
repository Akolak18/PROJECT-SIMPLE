BUILDING_IMAGES = [
    "/static/images/utcafront2.png",
    "/static/images/utcafront.png",
    "/static/images/Belsőudvar.png",
    "/static/images/utcafront3.png",
]

def _desc_kis(emelet, erdelytipus="erkéllyel"):
    return (
        f"Modern, kompakt 1 szobás lakás a Lujza Residence új építésű társasházban, "
        f"a {emelet}. emeleten. Tágas {erdelytipus}, beépített szekrények, "
        f"korszerű étkezőkonyha, elegáns fürdőszoba. Padlófűtés az egész lakásban, "
        f"klímarendszer-előkészítéssel. Ideális első otthonnak vagy befektetési célra – "
        f"a VIII. kerület dinamikusan fejlődő, könnyen értékesíthető ingatlanpiacon."
    )

def _desc_kozepes(emelet, erdelytipus="loggával"):
    return (
        f"Kényelmes 2 szobás lakás (nappali + hálószoba) a Lujza Residence társasházban, "
        f"a {emelet}. emeleten. Tágas, napfényes nappali {erdelytipus}, "
        f"korszerű beépített konyha, elegáns fürdőszoba. "
        f"Padlófűtés, klímarendszer-előkészítés. "
        f"Kiváló közlekedési kapcsolatok: metró, villamos és buszok közvetlen közelben."
    )

def _desc_nagy(emelet):
    return (
        f"Tágas, 3 szobás prémium lakás a Lujza Residence társasházban, "
        f"a {emelet}. emeleten. Nappali + 2 hálószoba elrendezés, "
        f"külön teakonyha, gardróbszoba és erkély. "
        f"A legmagasabb minőségű kivitelezés: padlófűtés, klímarendszer, "
        f"beépített szekrények, prémium burkolatok. "
        f"Ideális választás családok számára – tágas, jól átgondolt alaprajz."
    )

PROPERTIES = [

    # ── I. EMELET ─────────────────────────────────────────────────────────
    {
        "id": 1, "slug": "a01-i-emelet-nagy",
        "cim": "A/1 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/1 lakás (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 79, "szobak": 3, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy(1),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Teakonyha", "Gardróbszoba", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 2, "slug": "a02-i-emelet-kozepes",
        "cim": "A/2 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/2 lakás (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 45, "szobak": 2, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(1, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 3, "slug": "a03-i-emelet-kis",
        "cim": "A/3 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/3 lakás (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(1),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 4, "slug": "a04-i-emelet-kis",
        "cim": "A/4 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/4 lakás (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(1),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ── II. EMELET ────────────────────────────────────────────────────────
    {
        "id": 5, "slug": "a05-ii-emelet-nagy",
        "cim": "A/5 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/5 lakás (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 79, "szobak": 3, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy(2),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Teakonyha", "Gardróbszoba", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 6, "slug": "a06-ii-emelet-kozepes",
        "cim": "A/6 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/6 lakás (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 45, "szobak": 2, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(2, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 7, "slug": "a07-ii-emelet-kis",
        "cim": "A/7 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/7 lakás (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(2),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 8, "slug": "a08-ii-emelet-kis",
        "cim": "A/8 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/8 lakás (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(2),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ── III. EMELET ───────────────────────────────────────────────────────
    {
        "id": 9, "slug": "a09-iii-emelet-nagy",
        "cim": "A/9 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/9 lakás (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 79, "szobak": 3, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy(3),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Teakonyha", "Gardróbszoba", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "Kiemelt", "energiaosztaly": "A+",
    },
    {
        "id": 10, "slug": "a10-iii-emelet-kozepes",
        "cim": "A/10 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/10 lakás (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 48, "szobak": 2, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(3, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 11, "slug": "a11-iii-emelet-kis",
        "cim": "A/11 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/11 lakás (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(3),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 12, "slug": "a12-iii-emelet-kis",
        "cim": "A/12 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/12 lakás (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(3),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ── IV. EMELET ────────────────────────────────────────────────────────
    {
        "id": 13, "slug": "a13-iv-emelet-nagy",
        "cim": "A/13 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/13 lakás (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 79, "szobak": 3, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy(4),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Teakonyha", "Gardróbszoba", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "Kiemelt", "energiaosztaly": "A+",
    },
    {
        "id": 14, "slug": "a14-iv-emelet-kozepes",
        "cim": "A/14 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/14 lakás (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 48, "szobak": 2, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(4, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 15, "slug": "a15-iv-emelet-kis",
        "cim": "A/15 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/15 lakás (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(4),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 16, "slug": "a16-iv-emelet-kis",
        "cim": "A/16 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/16 lakás (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(4),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ── V. EMELET ─────────────────────────────────────────────────────────
    {
        "id": 17, "slug": "a17-v-emelet-tetoterasszal",
        "cim": "A/17 – V. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/17 lakás (V. emelet, tetőterasz)",
        "tipus": "Lakás", "ar": 0, "terulet": 72, "szobak": 2, "furdoszoba": 1,
        "emelet": 5, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": (
            "Egyedi, 2 szobás lakás hatalmas tetőterasszal az ötödik emeleten. "
            "A 71,98 m² hasznos alapterületű ingatlan Budapest egyik legkülönlegesebb "
            "új lakása – a tágas tetőterasz nyárikonyha kialakítására is alkalmas, "
            "és lenyűgöző kilátást biztosít a városra. "
            "Prémium kivitelezés: padlófűtés, klímarendszer, beépített szekrények. "
            "Ritka lehetőség – ilyen lakás kevés van!"
        ),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Tetőterasz", "Padlófűtés", "Klíma", "Lift", "Mélygarázs", "Panoráma kilátás"],
        "cimke": "Egyedi", "energiaosztaly": "A+",
    },
    {
        "id": 18, "slug": "a18-v-emelet-kozepes",
        "cim": "A/18 – V. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/18 lakás (V. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 48, "szobak": 2, "furdoszoba": 1,
        "emelet": 5, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(5, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 19, "slug": "a19-v-emelet-kis",
        "cim": "A/19 – V. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/19 lakás (V. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 36, "szobak": 1, "furdoszoba": 1,
        "emelet": 5, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(5, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ── VI. EMELET ────────────────────────────────────────────────────────
    {
        "id": 20, "slug": "a20-vi-emelet-nagy",
        "cim": "A/20 – VI. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/20 lakás (VI. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 50, "szobak": 2, "furdoszoba": 1,
        "emelet": 6, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": (
            "Prémium 2 szobás lakás a Lujza Residence legfelső emeletén. "
            "Hatodik emeleti elhelyezkedés, lenyűgöző kilátással Budapestre. "
            "Modern, tágas alaprajz, padlófűtés, klímarendszer. "
            "Exkluzív tetőszinti helyszín – Budapest legjobb befektetései közé tartozik."
        ),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "Prémium", "energiaosztaly": "A+",
    },
    {
        "id": 21, "slug": "a21-vi-emelet-kozepes",
        "cim": "A/21 – VI. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/21 lakás (VI. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 43, "szobak": 2, "furdoszoba": 1,
        "emelet": 6, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": (
            "Elegáns 2 szobás lakás a Lujza Residence hatodik emeletén. "
            "Kompakt, jól kialakított alaprajz, erkéllyel és panorámás kilátással. "
            "Padlófűtés, klímarendszer, prémium burkolatok. "
            "Kiváló lehetőség befektetésnek vagy fiatal pároknak."
        ),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "Prémium", "energiaosztaly": "A+",
    },
    {
        "id": 22, "slug": "a22-vi-emelet-kozepes",
        "cim": "A/22 – VI. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/22 lakás (VI. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 41, "szobak": 2, "furdoszoba": 1,
        "emelet": 6, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": (
            "Modern 2 szobás lakás a Lujza Residence hatodik emeletén. "
            "Erkéllyel, panorámás városi kilátással. Padlófűtés, klímarendszer. "
            "Az épület legmagasabban fekvő lakásainak egyike – csendes, exkluzív légkör."
        ),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély", "Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "Prémium", "energiaosztaly": "A+",
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
    results = list(PROPERTIES)
    if helyszin:
        h = helyszin.lower()
        results = [p for p in results if h in p["helyszin"].lower() or h in p["kerulet"].lower()]
    if tipus:
        results = [p for p in results if p["tipus"] == tipus]
    if ar_max is not None:
        results = [p for p in results if p["ar"] == 0 or p["ar"] <= ar_max]
    if szobak_min is not None:
        results = [p for p in results if p["szobak"] >= szobak_min]
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
