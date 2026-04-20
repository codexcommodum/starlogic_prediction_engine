"""
Starlogic - Theme Bridge
Maps ZWDS palace/star signals to Hellenistic house/planet signals
so both systems can agree (or disagree) on the same underlying theme.

Architecture:
- ZWDS is the primary narrator (rich palace + star + age-specific content)
- Hellenistic is the confidence validator (timing precision, dignity)
- When both point to the same theme, confidence = HIGH
- When only ZWDS points to it, confidence = LOW
- When one strong Hellenistic corroboration (tight aspect to sect light, dignified lord) = HIGH alone
"""

# Semantic themes used across both systems
THEMES = [
    "partnership",
    "wealth_gain",
    "property_home",
    "career_pivot",
    "health_event",
    "uprooting_travel",
    "friends_network",
    "transformation_loss",
    "family_parents",
    "creative_children",
    "identity_self",
    "hidden_endings",
]


# ZWDS palace + star combinations that signal each theme
ZWDS_THEME_SIGNALS = {
    "partnership": {
        "palaces": ["Spouse"],
        "stars_in_palace": {
            "Spouse": ["tan_lang", "tian_xiang", "tai_yin", "tian_tong", "tian_ji", "ju_men"],
        },
        "annual_palace_bonus": ["Spouse"],
    },
    "wealth_gain": {
        "palaces": ["Wealth"],
        "stars_in_palace": {
            "Wealth": ["wu_qu", "tian_fu", "zi_wei", "tai_yin", "tan_lang"],
        },
        "annual_palace_bonus": ["Wealth", "Property"],
    },
    "property_home": {
        "palaces": ["Property", "Travel"],
        "stars_in_palace": {
            "Property": ["tian_fu", "tai_yin", "zi_wei"],
            "Travel": ["po_jun", "tian_ji", "tai_yang"],
        },
        "annual_palace_bonus": ["Property", "Travel"],
    },
    "career_pivot": {
        "palaces": ["Career"],
        "stars_in_palace": {
            "Career": ["qi_sha", "wu_qu", "zi_wei", "tian_xiang", "po_jun"],
        },
        "annual_palace_bonus": ["Career"],
    },
    "health_event": {
        "palaces": ["Health"],
        "stars_in_palace": {
            "Health": ["qi_sha", "ju_men", "po_jun", "tian_liang", "lian_zhen"],
            "Life": ["qi_sha", "ju_men", "po_jun"],
        },
        "annual_palace_bonus": ["Health", "Life"],
    },
    "uprooting_travel": {
        "palaces": ["Travel"],
        "stars_in_palace": {
            "Travel": ["po_jun", "tian_ji", "tai_yang", "qi_sha"],
        },
        "annual_palace_bonus": ["Travel", "Property"],
    },
    "friends_network": {
        "palaces": ["Friends"],
        "stars_in_palace": {
            "Friends": ["tan_lang", "ju_men", "lian_zhen", "tian_tong"],
        },
        "annual_palace_bonus": ["Friends"],
    },
    "transformation_loss": {
        "palaces": ["Fortune", "Life"],
        "stars_in_palace": {
            "Fortune": ["qi_sha", "po_jun", "lian_zhen"],
            "Life": ["qi_sha", "po_jun"],
        },
        "annual_palace_bonus": ["Fortune"],
    },
    "family_parents": {
        "palaces": ["Parents"],
        "stars_in_palace": {
            "Parents": ["tai_yin", "tai_yang", "tian_liang", "tian_tong"],
        },
        "annual_palace_bonus": ["Parents"],
    },
    "creative_children": {
        "palaces": ["Children"],
        "stars_in_palace": {
            "Children": ["tian_xiang", "tan_lang", "tian_tong", "tai_yin"],
        },
        "annual_palace_bonus": ["Children"],
    },
    "identity_self": {
        "palaces": ["Life"],
        "stars_in_palace": {
            "Life": ["zi_wei", "tian_fu", "tai_yang", "tai_yin"],
        },
        "annual_palace_bonus": ["Life"],
    },
    "hidden_endings": {
        "palaces": [],
        "stars_in_palace": {},
        "annual_palace_bonus": [],
    },
}


# Hellenistic houses that corroborate each theme
# Strong = tight aspect to sect light OR dignified profection lord in this house
# Moderate = profection of this house OR lord's natal house
HELLENISTIC_THEME_SIGNALS = {
    "partnership":        {"primary_houses": [7], "secondary_houses": [5, 11]},
    "wealth_gain":        {"primary_houses": [2], "secondary_houses": [8, 11]},
    "property_home":      {"primary_houses": [4], "secondary_houses": [2, 10]},
    "career_pivot":       {"primary_houses": [10], "secondary_houses": [1, 6]},
    "health_event":       {"primary_houses": [6, 1], "secondary_houses": [8, 12]},
    "uprooting_travel":   {"primary_houses": [9, 3], "secondary_houses": [4]},
    "friends_network":    {"primary_houses": [11], "secondary_houses": [3]},
    "transformation_loss":{"primary_houses": [8], "secondary_houses": [12, 4]},
    "family_parents":     {"primary_houses": [4, 10], "secondary_houses": [3]},
    "creative_children":  {"primary_houses": [5], "secondary_houses": [9]},
    "identity_self":      {"primary_houses": [1], "secondary_houses": [10]},
    "hidden_endings":     {"primary_houses": [12], "secondary_houses": [4, 8]},
}


def detect_zwds_themes(year_data: dict) -> dict:
    """
    Inspect ZWDS annual + decade palace signals for this year.
    Returns dict of {theme_name: {"score": float, "evidence": [list of strings]}}
    Only themes actually signaled appear in the return.
    """
    detected = {}

    annual = year_data.get("annual", {})
    decade = year_data.get("decade", {})

    annual_palace = annual.get("palace_name", "")
    annual_stars = [s.lower() for s in (annual.get("stars_pinyin", annual.get("stars", [])) or [])]
    if isinstance(annual_stars, str):
        annual_stars = [s.strip().lower() for s in annual_stars.split() if s.strip()]

    decade_palace = decade.get("palace_name", "")
    decade_stars = [s.lower() for s in (decade.get("stars_pinyin", decade.get("stars", [])) or [])]
    if isinstance(decade_stars, str):
        decade_stars = [s.strip().lower() for s in decade_stars.split() if s.strip()]

    for theme, signals in ZWDS_THEME_SIGNALS.items():
        score = 0.0
        evidence = []

        # Check annual palace for theme-signaling stars
        for palace_name, target_stars in signals.get("stars_in_palace", {}).items():
            if annual_palace == palace_name:
                matching = [s for s in annual_stars if s in target_stars]
                if matching:
                    score += 0.6
                    evidence.append(f"annual palace {palace_name} has {', '.join(matching)}")

            if decade_palace == palace_name:
                matching = [s for s in decade_stars if s in target_stars]
                if matching:
                    score += 0.4
                    evidence.append(f"decade palace {palace_name} has {', '.join(matching)}")

        # Bonus for the annual palace itself matching the theme's primary palace
        if annual_palace in signals.get("annual_palace_bonus", []):
            score += 0.2
            evidence.append(f"annual palace is {annual_palace}")

        if score > 0:
            detected[theme] = {"score": round(score, 2), "evidence": evidence}

    return detected


def validate_with_hellenistic(theme: str, year_data: dict) -> dict:
    """
    For a given ZWDS-detected theme, check whether Hellenistic corroborates.
    Returns {"strength": "STRONG"|"MODERATE"|"NONE", "evidence": [strings]}
    """
    hel_signals = HELLENISTIC_THEME_SIGNALS.get(theme, {})
    primary_houses = hel_signals.get("primary_houses", [])
    secondary_houses = hel_signals.get("secondary_houses", [])

    prof = year_data.get("profection", {})
    aspects = year_data.get("aspects", [])

    evidence = []
    strength_points = 0

    prof_house = prof.get("house", 0)
    lord_house = prof.get("lord_house", 0)
    lord_dignity = prof.get("lord_dignity", "peregrine").lower()

    # Primary house profection = strong corroboration
    if prof_house in primary_houses:
        strength_points += 2
        evidence.append(f"profection is H{prof_house} (primary house for this theme)")

    # Lord's natal house in primary = moderate corroboration
    if lord_house in primary_houses:
        strength_points += 2
        evidence.append(f"year lord is natally in H{lord_house}")

    # Dignified lord = stronger
    if lord_dignity in ("exaltation", "domicile") and (prof_house in primary_houses or lord_house in primary_houses):
        strength_points += 1
        evidence.append(f"year lord is {lord_dignity} (delivers cleanly)")

    # Fallen lord on primary = frustrated version of the theme (still corroborates the theme)
    if lord_dignity in ("fall", "detriment") and (prof_house in primary_houses or lord_house in primary_houses):
        strength_points += 1
        evidence.append(f"year lord is {lord_dignity} (frustrated expression)")

    # Secondary house = weak corroboration
    if prof_house in secondary_houses:
        strength_points += 1
        evidence.append(f"profection is H{prof_house} (secondary house for this theme)")
    if lord_house in secondary_houses:
        strength_points += 1
        evidence.append(f"year lord is natally in H{lord_house} (secondary)")

    # Tight aspect (orb < 1) involving sect light, to a primary house = strong
    for asp in aspects:
        orb = asp.get("orb", 10)
        other_house = asp.get("other_house", 0)
        is_sect = asp.get("is_sect_light", False)

        if orb < 1.0 and other_house in primary_houses:
            strength_points += 2
            ev = f"tight {asp.get('aspect_type','aspect')} orb {orb}° to H{other_house}"
            if is_sect:
                ev += " (sect light)"
                strength_points += 1
            evidence.append(ev)
        elif orb < 2.0 and other_house in primary_houses:
            strength_points += 1
            evidence.append(f"aspect orb {orb}° to H{other_house}")

    # Map strength points to label
    if strength_points >= 3:
        strength = "STRONG"
    elif strength_points >= 1:
        strength = "MODERATE"
    else:
        strength = "NONE"

    return {"strength": strength, "points": strength_points, "evidence": evidence}


def compute_confidence(zwds_score: float, hellenistic: dict) -> str:
    """
    Determine confidence label from ZWDS strength + Hellenistic corroboration.
    Returns "HIGH" | "MEDIUM" | "LOW"
    """
    strength = hellenistic.get("strength", "NONE")

    # STRONG Hellenistic alone can be HIGH even with moderate ZWDS
    if strength == "STRONG" and zwds_score >= 0.4:
        return "HIGH"

    # MODERATE + solid ZWDS = MEDIUM
    if strength == "MODERATE" and zwds_score >= 0.4:
        return "MEDIUM"

    # Strong ZWDS alone with no Hellenistic = MEDIUM (ZWDS is narrative primary)
    if zwds_score >= 0.8 and strength == "NONE":
        return "MEDIUM"

    # Any ZWDS signal at all = LOW
    return "LOW"


def build_year_themes(year_data: dict) -> list:
    """
    For a given year, return ranked list of themes with confidence labels.
    Each entry: {"theme": str, "zwds_score": float, "zwds_evidence": [...],
                 "hellenistic_strength": str, "hellenistic_evidence": [...],
                 "confidence": "HIGH"|"MEDIUM"|"LOW"}
    """
    zwds_themes = detect_zwds_themes(year_data)
    results = []

    for theme, zwds_data in zwds_themes.items():
        hel = validate_with_hellenistic(theme, year_data)
        confidence = compute_confidence(zwds_data["score"], hel)

        results.append({
            "theme": theme,
            "zwds_score": zwds_data["score"],
            "zwds_evidence": zwds_data["evidence"],
            "hellenistic_strength": hel["strength"],
            "hellenistic_evidence": hel["evidence"],
            "confidence": confidence,
        })

    # Sort by confidence then score
    confidence_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    results.sort(key=lambda r: (-confidence_order[r["confidence"]], -r["zwds_score"]))

    return results


def is_compression_year(themes: list) -> bool:
    """
    New compression definition: 3+ themes each at MEDIUM or HIGH confidence in one year.
    """
    strong_themes = [t for t in themes if t["confidence"] in ("HIGH", "MEDIUM")]
    return len(strong_themes) >= 3
