"""
Starlogic - Theme Bridge (v2)

ZWDS-led theme detection with Hellenistic confidence validation.
Now includes:
  - Sihua (Four Transformations) activation — the core ZWDS mechanic
  - Age-bracket filtering — themes that don't apply at certain life stages
  - Expanded Hellenistic corroboration — planet/aspect/Venus/Moon checks
"""

from sihua import compute_year_sihua, sihua_activated_themes, extract_stem_from_year_pillar, SIHUA_VALENCE


THEMES = [
    "partnership", "wealth_gain", "property_home", "career_pivot", "health_event",
    "uprooting_travel", "friends_network", "transformation_loss", "family_parents",
    "creative_children", "identity_self", "hidden_endings",
]


# Age-bracket filter: which themes can fire at which ages.
# Universal rule — a child doesn't have a career, a senior rarely has new partnerships.
# Themes not listed here fire at all ages.
AGE_BRACKET_FILTER = {
    "career_pivot":      {"min_age": 14, "max_age": 999},   # career only from teens
    "creative_children": {"min_age": 18, "max_age": 999},   # having children starts adulthood
    "wealth_gain":       {"min_age": 14, "max_age": 999},   # kids don't earn meaningfully
    "partnership":       {"min_age": 4,  "max_age": 999},   # first crushes allowed from 4
}


# ZWDS palace/star signals (from annual + decade palace)
ZWDS_THEME_SIGNALS = {
    "partnership": {
        "stars_in_palace": {"Spouse": ["tan_lang", "tian_xiang", "tai_yin", "tian_tong", "tian_ji", "ju_men"]},
        "annual_palace_bonus": ["Spouse"],
    },
    "wealth_gain": {
        "stars_in_palace": {"Wealth": ["wu_qu", "tian_fu", "zi_wei", "tai_yin", "tan_lang"]},
        "annual_palace_bonus": ["Wealth", "Property"],
    },
    "property_home": {
        "stars_in_palace": {
            "Property": ["tian_fu", "tai_yin", "zi_wei"],
            "Travel":   ["po_jun", "tian_ji", "tai_yang"],
        },
        "annual_palace_bonus": ["Property", "Travel"],
    },
    "career_pivot": {
        "stars_in_palace": {"Career": ["qi_sha", "wu_qu", "zi_wei", "tian_xiang", "po_jun"]},
        "annual_palace_bonus": ["Career"],
    },
    "health_event": {
        "stars_in_palace": {
            "Health": ["qi_sha", "ju_men", "po_jun", "tian_liang", "lian_zhen"],
            "Life":   ["qi_sha", "ju_men", "po_jun"],
        },
        "annual_palace_bonus": ["Health", "Life"],
    },
    "uprooting_travel": {
        "stars_in_palace": {"Travel": ["po_jun", "tian_ji", "tai_yang", "qi_sha"]},
        "annual_palace_bonus": ["Travel", "Property"],
    },
    "friends_network": {
        "stars_in_palace": {"Friends": ["tan_lang", "ju_men", "lian_zhen", "tian_tong"]},
        "annual_palace_bonus": ["Friends"],
    },
    "transformation_loss": {
        "stars_in_palace": {
            "Fortune": ["qi_sha", "po_jun", "lian_zhen"],
            "Life":    ["qi_sha", "po_jun"],
        },
        "annual_palace_bonus": ["Fortune"],
    },
    "family_parents": {
        "stars_in_palace": {"Parents": ["tai_yin", "tai_yang", "tian_liang", "tian_tong"]},
        "annual_palace_bonus": ["Parents"],
    },
    "creative_children": {
        "stars_in_palace": {"Children": ["tian_xiang", "tan_lang", "tian_tong", "tai_yin"]},
        "annual_palace_bonus": ["Children"],
    },
    "identity_self": {
        "stars_in_palace": {"Life": ["zi_wei", "tian_fu", "tai_yang", "tai_yin"]},
        "annual_palace_bonus": ["Life"],
    },
    "hidden_endings": {
        "stars_in_palace": {},
        "annual_palace_bonus": [],
    },
}


# Hellenistic houses + planetary signatures per theme.
# Expanded beyond just profection houses.
HELLENISTIC_THEME_SIGNALS = {
    "partnership":        {"primary_houses": [7], "secondary_houses": [5, 11], "planets": ["Venus", "Moon"]},
    "wealth_gain":        {"primary_houses": [2], "secondary_houses": [8, 11], "planets": ["Venus", "Jupiter"]},
    "property_home":      {"primary_houses": [4], "secondary_houses": [2, 10], "planets": ["Moon", "Saturn"]},
    "career_pivot":       {"primary_houses": [10], "secondary_houses": [1, 6], "planets": ["Sun", "Saturn", "Mars"]},
    "health_event":       {"primary_houses": [6, 1], "secondary_houses": [8, 12], "planets": ["Mars", "Saturn"]},
    "uprooting_travel":   {"primary_houses": [9, 3], "secondary_houses": [4], "planets": ["Mercury", "Jupiter"]},
    "friends_network":    {"primary_houses": [11], "secondary_houses": [3], "planets": ["Jupiter", "Venus"]},
    "transformation_loss":{"primary_houses": [8], "secondary_houses": [12, 4], "planets": ["Mars", "Saturn", "Pluto"]},
    "family_parents":     {"primary_houses": [4, 10], "secondary_houses": [3], "planets": ["Moon", "Saturn"]},
    "creative_children":  {"primary_houses": [5], "secondary_houses": [9], "planets": ["Venus", "Jupiter", "Moon"]},
    "identity_self":      {"primary_houses": [1], "secondary_houses": [10], "planets": ["Sun", "Moon"]},
    "hidden_endings":     {"primary_houses": [12], "secondary_houses": [4, 8], "planets": ["Saturn", "Neptune"]},
}


def _parse_palace_stars(palace_data: dict) -> list:
    """Normalize palace star representation to pinyin list."""
    stars = palace_data.get("stars_pinyin", palace_data.get("stars", []))
    if isinstance(stars, str):
        return [s.strip().lower() for s in stars.split() if s.strip()]
    if isinstance(stars, list):
        return [s.lower() if isinstance(s, str) else s.get("pinyin", "").lower() for s in stars]
    return []


def detect_zwds_themes(year_data: dict, natal_palaces: list) -> dict:
    """
    Detect themes from:
      1. Annual palace + decade palace stars (existing logic)
      2. Sihua transformations (NEW) — year stem activates natal palaces

    Returns dict of {theme: {"score": float, "evidence": [...], "sihua_via": optional dict}}
    """
    detected = {}

    annual = year_data.get("annual", {})
    decade = year_data.get("decade", {})

    annual_palace = annual.get("palace_name", "")
    annual_stars = _parse_palace_stars(annual)
    decade_palace = decade.get("palace_name", "")
    decade_stars = _parse_palace_stars(decade)

    # Layer A: annual/decade palace-star matching (existing)
    for theme, signals in ZWDS_THEME_SIGNALS.items():
        score = 0.0
        evidence = []

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

        if annual_palace in signals.get("annual_palace_bonus", []):
            score += 0.2
            evidence.append(f"annual palace is {annual_palace}")

        if score > 0:
            detected[theme] = {"score": round(score, 2), "evidence": evidence}

    # Layer B: sihua transformations (NEW)
    # Extract year stem from "Ren Wu" -> "Ren"
    year_stem = extract_stem_from_year_pillar(annual.get("year_stem_branch", ""))
    if year_stem and natal_palaces:
        sihua_data = compute_year_sihua(year_stem, natal_palaces)
        activations = sihua_activated_themes(sihua_data)

        for act in activations:
            theme = act["theme"]
            via = act["via"]
            palace = act["palace"]
            star = act["star"]
            flavor = act["flavor"]

            # Scoring by transformation type:
            # lu = +0.7 (strong favorable)
            # quan = +0.7 (strong forceful)
            # ji = +0.7 (strong obstruction — still scored high because event is happening)
            # ke = +0.4 (moderate recognition)
            sihua_score = 0.7 if via in ("lu", "quan", "ji") else 0.4

            if theme not in detected:
                detected[theme] = {"score": 0.0, "evidence": [], "sihua": []}
            else:
                detected[theme].setdefault("sihua", [])

            detected[theme]["score"] = round(detected[theme]["score"] + sihua_score, 2)
            detected[theme]["evidence"].append(
                f"sihua {via.upper()} transforms {star} into natal {palace} ({flavor})"
            )
            detected[theme]["sihua"].append({
                "type": via, "star": star, "palace": palace, "flavor": flavor,
                "valence": SIHUA_VALENCE[via],
            })

    return detected


def validate_with_hellenistic(theme: str, year_data: dict, natal_planets: list = None) -> dict:
    """
    Check whether Hellenistic corroborates a ZWDS-detected theme.
    Now includes: profection houses, aspect houses, AND natal planet involvement.
    """
    hel_signals = HELLENISTIC_THEME_SIGNALS.get(theme, {})
    primary_houses = hel_signals.get("primary_houses", [])
    secondary_houses = hel_signals.get("secondary_houses", [])
    theme_planets = hel_signals.get("planets", [])

    prof = year_data.get("profection", {})
    aspects = year_data.get("aspects", [])

    evidence = []
    strength_points = 0

    prof_house = prof.get("house", 0)
    lord_house = prof.get("lord_house", 0)
    lord_name = prof.get("lord", "")
    lord_dignity = prof.get("lord_dignity", "peregrine").lower()

    # Year lord IS a theme-planet — strong corroboration
    if lord_name in theme_planets:
        strength_points += 2
        evidence.append(f"year lord is {lord_name} (theme-aligned planet)")

    # Primary house profection
    if prof_house in primary_houses:
        strength_points += 2
        evidence.append(f"profection is H{prof_house} (primary)")

    # Lord's natal house
    if lord_house in primary_houses:
        strength_points += 2
        evidence.append(f"year lord natally in H{lord_house}")

    # Dignity modifier on primary
    if lord_dignity in ("exaltation", "domicile") and (prof_house in primary_houses or lord_house in primary_houses):
        strength_points += 1
        evidence.append(f"lord {lord_dignity}")
    if lord_dignity in ("fall", "detriment") and (prof_house in primary_houses or lord_house in primary_houses):
        strength_points += 1
        evidence.append(f"lord {lord_dignity} (frustrated)")

    # Secondary houses
    if prof_house in secondary_houses:
        strength_points += 1
        evidence.append(f"profection is H{prof_house} (secondary)")
    if lord_house in secondary_houses:
        strength_points += 1
        evidence.append(f"lord natally in H{lord_house} (secondary)")

    # Aspect-based corroboration
    for asp in aspects:
        orb = asp.get("orb", 10)
        other_house = asp.get("other_house", 0)
        other_planet = asp.get("other_planet", "")
        is_sect = asp.get("is_sect_light", False)

        # Tight aspect to primary house
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

        # Tight aspect to theme-aligned planet
        if orb < 1.0 and other_planet in theme_planets:
            strength_points += 2
            evidence.append(f"tight aspect to natal {other_planet}")

    if strength_points >= 3:
        strength = "STRONG"
    elif strength_points >= 1:
        strength = "MODERATE"
    else:
        strength = "NONE"

    return {"strength": strength, "points": strength_points, "evidence": evidence}


def compute_confidence(zwds_score: float, hellenistic: dict) -> str:
    strength = hellenistic.get("strength", "NONE")
    if strength == "STRONG" and zwds_score >= 0.4:
        return "HIGH"
    if strength == "MODERATE" and zwds_score >= 0.4:
        return "MEDIUM"
    if zwds_score >= 0.8 and strength == "NONE":
        return "MEDIUM"
    if zwds_score >= 0.4 and strength == "NONE":
        return "LOW"
    if zwds_score >= 0.2 and strength == "MODERATE":
        return "LOW"
    return "LOW"


def _passes_age_filter(theme: str, age: int) -> bool:
    """True if this theme is allowed to fire at this age."""
    f = AGE_BRACKET_FILTER.get(theme)
    if not f:
        return True
    return f["min_age"] <= age <= f["max_age"]


def build_year_themes(year_data: dict, natal_palaces: list = None, natal_planets: list = None) -> list:
    """
    Returns ranked list of themes with confidence labels.
    Signature backward-compatible: if natal_palaces is None, sihua is skipped.
    """
    age = year_data.get("age", 0)
    zwds_themes = detect_zwds_themes(year_data, natal_palaces or [])

    results = []
    for theme, zwds_data in zwds_themes.items():
        if not _passes_age_filter(theme, age):
            continue

        hel = validate_with_hellenistic(theme, year_data, natal_planets)
        confidence = compute_confidence(zwds_data["score"], hel)

        entry = {
            "theme": theme,
            "zwds_score": zwds_data["score"],
            "zwds_evidence": zwds_data["evidence"],
            "hellenistic_strength": hel["strength"],
            "hellenistic_evidence": hel["evidence"],
            "confidence": confidence,
        }
        if "sihua" in zwds_data:
            entry["sihua"] = zwds_data["sihua"]
        results.append(entry)

    confidence_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    results.sort(key=lambda r: (-confidence_order[r["confidence"]], -r["zwds_score"]))
    return results


def is_compression_year(themes: list) -> bool:
    """3+ themes at MEDIUM or HIGH confidence in one year."""
    strong_themes = [t for t in themes if t["confidence"] in ("HIGH", "MEDIUM")]
    return len(strong_themes) >= 3
