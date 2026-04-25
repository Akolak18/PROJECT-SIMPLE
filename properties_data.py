BUILDING_IMAGES = [
    "/static/images/utcafront2.png",
    "/static/images/utcafront.png",
    "/static/images/Belsőudvar.png",
    "/static/images/utcafront3.png",
]


def _desc_kis(emelet, erkely_m2, erkely_tip="erkéllyel"):
    return (
        f"Modern, 1 szobás lakás a Lujza Residence új építésű társasházban, "
        f"a {emelet}. emeleten. Tágas {erkely_m2} m² {erkely_tip}, beépített szekrények, "
        f"korszerű konyha, elegáns fürdőszoba. Padlófűtés az egész lakásban, "
        f"klímarendszer-előkészítéssel. Ideális első otthonnak vagy befektetési célra."
    )


def _desc_kozepes(emelet, terulet, erkely_m2, erkely_tip="loggával"):
    return (
        f"Kényelmes 2 szobás lakás a Lujza Residence társasházban, "
        f"a {emelet}. emeleten ({terulet} m² hasznos alapterület, {erkely_m2} m² {erkely_tip}). "
        f"Napfényes nappali, korszerű beépített konyha, elegáns fürdőszoba. "
        f"Padlófűtés, klímarendszer-előkészítés. "
        f"Kiváló közlekedési kapcsolatok: metró, villamos és buszok közvetlen közelben."
    )


def _desc_nagy_erkelyes(emelet, terulet, erkely_m2):
    return (
        f"Tágas {terulet} m²-es lakás a Lujza Residence társasházban, "
        f"a {emelet}. emeleten, hatalmas {erkely_m2} m²-es erkéllyel. "
        f"Napfényes nappali-étkező, 2 hálószoba, elegáns fürdőszoba, beépített szekrények. "
        f"Padlófűtés, klímarendszer-előkészítés. "
        f"Kiváló közlekedési kapcsolatok: metró, villamos és buszok közvetlen közelben."
    )


def _desc_penthouse(emelet, terulet, tetoterasszal_m2):
    return (
        f"Egyedi {terulet} m²-es lakás hatalmas, {tetoterasszal_m2} m²-es privát tetőterasszal "
        f"a {emelet}. emeleten. Lenyűgöző panoráma Budapestre – nyárikonyha és pihenőtér "
        f"kialakítási lehetőséggel. Prémium kivitelezés: padlófűtés, klímarendszer, "
        f"beépített szekrények. Ritka lehetőség – ilyen lakás kevés van az épületben!"
    )


def _desc_tetoszint_terasszal(emelet, terulet, tetoterasszal_m2):
    return (
        f"Exkluzív {terulet} m²-es lakás a Lujza Residence legfelső emeletén ({emelet}. emelet), "
        f"privát {tetoterasszal_m2} m²-es tetőterasszal. "
        f"Lenyűgöző panoráma Budapestre – nyárikonyha és pihenőtér kialakítási lehetőséggel. "
        f"Padlófűtés, klímarendszer, beépített szekrények. "
        f"Az épület egyik legexkluzívabb és legkeresettebb egysége."
    )


def _desc_tetoszint_erkely_terasszal(emelet, terulet, erkely_m2, tetoterasszal_m2):
    return (
        f"Különleges {terulet} m²-es lakás a Lujza Residence {emelet}. emeletén, "
        f"{erkely_m2} m²-es erkéllyel és {tetoterasszal_m2} m²-es privát tetőterasszal. "
        f"Két külső tér – ideális szabadtéri élet a városban. "
        f"Padlófűtés, klímarendszer-előkészítés, elegáns fürdőszoba. "
        f"Ritka kombináció az újépítésű piacon."
    )


PROPERTIES = [

    # ══════════════════════════════════════════════════════════════════════
    # I. EMELET  –  A/1 – A/5
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1, "slug": "a01-i-emelet",
        "cim": "A/1 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/1 (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 45, "szobak": 2, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(1, 44.93, 3.82, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (3,82 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 2, "slug": "a02-i-emelet",
        "cim": "A/2 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/2 (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 48, "szobak": 2, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(1, 47.58, 2.74, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (2,74 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 3, "slug": "a03-i-emelet",
        "cim": "A/3 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/3 (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(1, 5.09, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (5,09 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 4, "slug": "a04-i-emelet",
        "cim": "A/4 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/4 (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(1, 5.09, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (5,09 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 5, "slug": "a05-i-emelet",
        "cim": "A/5 – I. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/5 (I. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 1, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(1, 5.09, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (5,09 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ══════════════════════════════════════════════════════════════════════
    # II. EMELET  –  A/6 – A/10  (azonos az I. emelettel)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6, "slug": "a06-ii-emelet",
        "cim": "A/6 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/6 (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 45, "szobak": 2, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(2, 44.93, 3.82, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (3,82 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 7, "slug": "a07-ii-emelet",
        "cim": "A/7 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/7 (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 48, "szobak": 2, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(2, 47.58, 2.74, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (2,74 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 8, "slug": "a08-ii-emelet",
        "cim": "A/8 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/8 (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(2, 5.09, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (5,09 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 9, "slug": "a09-ii-emelet",
        "cim": "A/9 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/9 (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(2, 5.09, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (5,09 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 10, "slug": "a10-ii-emelet",
        "cim": "A/10 – II. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/10 (II. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 2, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(2, 5.09, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (5,09 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ══════════════════════════════════════════════════════════════════════
    # III. EMELET  –  A/11 – A/14
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11, "slug": "a11-iii-emelet",
        "cim": "A/11 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/11 (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 45, "szobak": 2, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(3, 44.93, 3.82, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (3,82 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 12, "slug": "a12-iii-emelet",
        "cim": "A/12 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/12 (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 48, "szobak": 2, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(3, 47.58, 2.74, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (2,74 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 13, "slug": "a13-iii-emelet",
        "cim": "A/13 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/13 (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(3, 4, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (4 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "Kiemelt", "energiaosztaly": "A+",
    },
    {
        "id": 14, "slug": "a14-iii-emelet",
        "cim": "A/14 – III. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/14 (III. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 70, "szobak": 2, "furdoszoba": 1,
        "emelet": 3, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy_erkelyes(3, 70.28, 10.22),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (10,22 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "Kiemelt", "energiaosztaly": "A+",
    },

    # ══════════════════════════════════════════════════════════════════════
    # IV. EMELET  –  A/15 – A/18  (azonos a III. emelettel)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15, "slug": "a15-iv-emelet",
        "cim": "A/15 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/15 (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 45, "szobak": 2, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(4, 44.93, 3.82, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (3,82 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 16, "slug": "a16-iv-emelet",
        "cim": "A/16 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/16 (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 48, "szobak": 2, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kozepes(4, 47.58, 2.74, "loggával"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Loggia (2,74 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 17, "slug": "a17-iv-emelet",
        "cim": "A/17 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/17 (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(4, 4, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (4 m²)", "Padlófűtés", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },
    {
        "id": 18, "slug": "a18-iv-emelet",
        "cim": "A/18 – IV. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/18 (IV. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 70, "szobak": 2, "furdoszoba": 1,
        "emelet": 4, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy_erkelyes(4, 70.28, 10.22),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (10,22 m²)", "Padlófűtés", "Lift", "Mélygarázs", "Klíma-előkészítés"],
        "cimke": "Kiemelt", "energiaosztaly": "A+",
    },

    # ══════════════════════════════════════════════════════════════════════
    # V. EMELET  –  A/19 – A/21
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 19, "slug": "a19-v-emelet-tetoterasszal", "elerheto": False,
        "cim": "A/19 – V. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/19 (V. emelet, tetőterasz)",
        "tipus": "Lakás", "ar": 0, "terulet": 72, "szobak": 2, "furdoszoba": 1,
        "emelet": 5, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_penthouse(5, 71.99, 37.32),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Tetőterasz (37,32 m²)", "Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "Egyedi", "energiaosztaly": "A+",
    },
    {
        "id": 20, "slug": "a20-v-emelet", "elerheto": False,
        "cim": "A/20 – V. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/20 (V. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 65, "szobak": 2, "furdoszoba": 1,
        "emelet": 5, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy_erkelyes(5, 65.47, 9.15),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (9,15 m²)", "Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "Prémium", "energiaosztaly": "A+",
    },
    {
        "id": 21, "slug": "a21-v-emelet", "elerheto": False,
        "cim": "A/21 – V. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/21 (V. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 35, "szobak": 1, "furdoszoba": 1,
        "emelet": 5, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_kis(5, 5.10, "erkéllyel"),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (5,10 m²)", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "", "energiaosztaly": "A+",
    },

    # ══════════════════════════════════════════════════════════════════════
    # VI. EMELET  –  A/22 – A/24
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 22, "slug": "a22-vi-emelet-tetoterasszal",
        "cim": "A/22 – VI. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/22 (VI. emelet, tetőterasz)",
        "tipus": "Lakás", "ar": 0, "terulet": 45, "szobak": 2, "furdoszoba": 1,
        "emelet": 6, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_tetoszint_terasszal(6, 44.87, 24.08),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Tetőterasz (24,08 m²)", "Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "Prémium", "energiaosztaly": "A+",
    },
    {
        "id": 23, "slug": "a23-vi-emelet-erkely-tetoterasszal",
        "cim": "A/23 – VI. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/23 (VI. emelet, erkély + tetőterasz)",
        "tipus": "Lakás", "ar": 0, "terulet": 47, "szobak": 2, "furdoszoba": 1,
        "emelet": 6, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_tetoszint_erkely_terasszal(6, 46.75, 4, 8),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (4 m²)", "Tetőterasz (8 m²)", "Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
        "cimke": "Prémium", "energiaosztaly": "A+",
    },
    {
        "id": 24, "slug": "a24-vi-emelet",
        "cim": "A/24 – VI. emelet", "helyszin": "Budapest", "kerulet": "VIII. kerület",
        "teljes_cim": "Lujza utca 24. – A/24 (VI. emelet)",
        "tipus": "Lakás", "ar": 0, "terulet": 40, "szobak": 2, "furdoszoba": 1,
        "emelet": 6, "epitesi_ev": 2026, "allapot": "Új építésű",
        "leiras": _desc_nagy_erkelyes(6, 40.12, 10.22),
        "kepek": BUILDING_IMAGES,
        "szolgaltatasok": ["Erkély (10,22 m²)", "Panoráma kilátás", "Padlófűtés", "Klíma", "Lift", "Mélygarázs"],
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
