"""
Starlogic - Sihua (Four Transformations) Engine

Canonical Zi Wei Dou Shu mechanic: each year's heavenly stem triggers
four specific stars to transform. Whatever palace each transformed star
sits in (natally) becomes activated for that year.

This is the CORE way ZWDS predicts event timing. Not optional.

Universal lookup table used by every Chinese astrologer for centuries.
Not tuned to any chart. Same table for everyone.

Reference: traditional 紫微斗数 sihua table, pinyin form.
"""

# Canonical stem -> (Lu, Quan, Ke, Ji) transformations
# Lu  = 化祿 wealth/prosperity — brings fortune, abundance
# Quan = 化權 power/authority — brings force, control, effort
# Ke  = 化科 recognition/reputation — brings visibility, study, protection
# Ji  = 化忌 obstruction/attachment — brings blockage, loss, hidden friction
SIHUA_TABLE = {
    "Jia":  {"lu": "lian_zhen", "quan": "po_jun",   "ke": "wu_qu",     "ji": "tai_yang"},
    "Yi":   {"lu": "tian_ji",   "quan": "tian_liang","ke": "zi_wei",   "ji": "tai_yin"},
    "Bing": {"lu": "tian_tong", "quan": "tian_ji",  "ke": "wen_chang", "ji": "lian_zhen"},
    "Ding": {"lu": "tai_yin",   "quan": "tian_tong","ke": "tian_ji",   "ji": "ju_men"},
    "Wu":   {"lu": "tan_lang",  "quan": "tai_yin",  "ke": "you_bi",    "ji": "tian_ji"},
    "Ji":   {"lu": "wu_qu",     "quan": "tan_lang", "ke": "tian_liang","ji": "wen_qu"},
    "Geng": {"lu": "tai_yang",  "quan": "wu_qu",    "ke": "tai_yin",   "ji": "tian_tong"},
    "Xin":  {"lu": "ju_men",    "quan": "tai_yang", "ke": "wen_qu",    "ji": "wen_chang"},
    "Ren":  {"lu": "tian_liang","quan": "zi_wei",   "ke": "zuo_fu",    "ji": "wu_qu"},
    "Gui":  {"lu": "po_jun",    "quan": "ju_men",   "ke": "tai_yin",   "ji": "tan_lang"},
}

# Transformation flavor descriptors (used by theme bridge)
TRANSFORMATION_FLAVOR = {
    "lu":   "fortune/abundance",
    "quan": "power/force",
    "ke":   "recognition/protection",
    "ji":   "obstruction/loss",
}

# Palace -> theme mapping for sihua activation
# When a sihua-transformed star lands in one of these palaces, these themes activate.
# Universal mapping — the Spouse palace activation means partnership for anyone.
PALACE_THEMES = {
    "Life":     ["identity_self"],
    "Siblings": ["friends_network"],
    "Spouse":   ["partnership"],
    "Children": ["creative_children"],
    "Wealth":   ["wealth_gain"],
    "Health":   ["health_event"],
    "Travel":   ["uprooting_travel", "property_home"],
    "Friends":  ["friends_network"],
    "Career":   ["career_pivot"],
    "Property": ["property_home", "wealth_gain"],
    "Fortune":  ["transformation_loss"],
    "Parents":  ["family_parents"],
}


def extract_stem_from_year_pillar(year_stem_branch: str) -> str:
    """
    Take 'Ren Wu' or 'Jia Zi' style string and return the stem ('Ren', 'Jia').
    Any chart, any year.
    """
    if not year_stem_branch:
        return ""
    parts = year_stem_branch.strip().split()
    return parts[0] if parts else ""


def find_natal_palace_for_star(star_pinyin: str, palaces: list) -> str:
    """
    Given a star pinyin, find which natal palace it sits in.
    Returns English palace name or empty string.
    Universal — reads the chart data as-is.
    """
    for p in palaces:
        stars = p.get("stars", [])
        for s in stars:
            if isinstance(s, dict):
                if s.get("pinyin") == star_pinyin:
                    return p.get("name_english", "")
            elif isinstance(s, str):
                if s == star_pinyin:
                    return p.get("name_english", "")
    return ""


def compute_year_sihua(year_stem: str, natal_palaces: list) -> dict:
    """
    Core function: given a year's stem and the chart's natal palaces,
    return which palaces activate via sihua this year and how.

    Returns:
        {
          "lu":   {"star": "tian_liang", "palace": "Parents", "flavor": "fortune/abundance"},
          "quan": {"star": "zi_wei",     "palace": "Wealth",  "flavor": "power/force"},
          "ke":   {"star": "zuo_fu",     "palace": "",        "flavor": "..."},  # empty if star isn't a natal main star
          "ji":   {"star": "wu_qu",      "palace": "Career",  "flavor": "obstruction/loss"},
        }

    If a sihua star doesn't sit in any natal palace (e.g., wen_chang, wen_qu, zuo_fu, you_bi
    are minor stars not always tracked), the palace is empty string — the transformation
    still happens but has no primary palace effect.
    """
    if year_stem not in SIHUA_TABLE:
        return {}

    transforms = SIHUA_TABLE[year_stem]
    result = {}
    for trans_type, star in transforms.items():
        palace = find_natal_palace_for_star(star, natal_palaces)
        result[trans_type] = {
            "star": star,
            "palace": palace,
            "flavor": TRANSFORMATION_FLAVOR[trans_type],
        }
    return result


def sihua_activated_themes(sihua_data: dict) -> list:
    """
    Convert sihua activations into a list of activated themes with flavor.
    Returns list of dicts: {"theme": str, "via": "lu|quan|ke|ji", "star": str, "palace": str}
    """
    activations = []
    for trans_type, data in sihua_data.items():
        palace = data.get("palace", "")
        if not palace:
            continue
        themes = PALACE_THEMES.get(palace, [])
        for theme in themes:
            activations.append({
                "theme": theme,
                "via": trans_type,
                "star": data["star"],
                "palace": palace,
                "flavor": data["flavor"],
            })
    return activations


# Valence adjustments per transformation type
# Lu and Quan favor the theme (delivered/empowered). Ji frustrates it (blocked/lost).
# Ke is mixed — brings recognition but also scrutiny.
SIHUA_VALENCE = {
    "lu":   "favorable",
    "quan": "forceful",
    "ke":   "visible",
    "ji":   "obstructed",
}
