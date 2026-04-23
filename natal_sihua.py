"""
natal_sihua.py
==============

Consumes the v2 starlogic_zwds_engine natal Sihua fields:
  - palace.birth_year_sihua   — 生年四化 (karmic baseline markers)
  - palace.self_hua           — 自化 (personality autopilots / leaks)
  - palace.incoming_sihua     — flying Sihua received from another palace's stem
  - palace.outgoing_sihua     — flying Sihua sent by this palace's stem

And the top-level field:
  - origin_palace_english     — 来因宫 (karmic root)

Produces a structured "natal_sihua_layer" dict that score_convergence
reads to emit specific findings like:
  "Wealth receives 忌 from Fortune palace — inner-life cost draining finances"

Design principles:
  * Backward compatible — if v2 fields are absent, returns an empty layer
    and score_convergence continues to operate on legacy keyword-only signals.
  * Maps Sihua types to the same domain keywords used in PALACE_THEMES so
    findings flow through the existing multi-source bonus curve.
  * Natal layer is computed ONCE per reading, not per year — but its
    findings weigh into EVERY year's score, because these are structural
    lifelong characteristics of the chart.
"""

from typing import Optional

# Sihua type → valence weight and action verb
# "lu"   = 禄 — flow, opportunity, gain (positive)
# "quan" = 权 — force, authority, mandatory action (positive but demanding)
# "ke"   = 科 — reputation, visibility, documentation (positive)
# "ji"   = 忌 — obstruction, loss, friction (negative)
SIHUA_META = {
    "lu":   {"weight": 0.25, "valence": "flow",       "action": "opens"},
    "quan": {"weight": 0.30, "valence": "force",      "action": "demands"},
    "ke":   {"weight": 0.20, "valence": "reputation", "action": "elevates"},
    "ji":   {"weight": 0.35, "valence": "obstruction","action": "obstructs"},
}


# Palace name → domain keywords (should mirror the orchestrator's PALACE_THEMES
# so new sources stack into existing domains, not orphan keywords).
PALACE_KEYWORDS = {
    "Life":     ["self", "identity", "body", "destiny", "personality"],
    "Siblings": ["peers", "rivalry", "social_identity", "belonging"],
    "Spouse":   ["partnerships", "marriage", "business_alliances"],
    "Children": ["creative_output", "offspring", "legacy", "production"],
    "Wealth":   ["assets", "accumulation", "financial_sovereignty"],
    "Health":   ["vitality", "emotional_stability", "body_signals"],
    "Travel":   ["movement", "change", "exploration", "relocation"],
    "Friends":  ["social_network", "benefactors", "professional_connections"],
    "Career":   ["profession", "public_role", "ambition", "authority"],
    "Property": ["real_estate", "home_base", "physical_foundation"],
    "Fortune":  ["luck", "fate", "blessings", "karmic_inheritance"],
    "Parents":  ["parental_influence", "authority_figures", "inherited_patterns"],
}


def _get_palace_english(p: dict) -> str:
    """Extract English palace name from a v2 zwds palace dict."""
    return p.get("name_english", "")


def _sihua_entries(p: dict, key: str) -> list:
    """Safely extract a sihua field as a list of dicts. Returns [] if absent."""
    value = p.get(key, [])
    if not isinstance(value, list):
        return []
    # Each entry is {"star": ..., "type": ...} for birth/self hua,
    # or {"from_palace"/"to_palace": ..., "star": ..., "type": ...} for flying.
    return [e for e in value if isinstance(e, dict)]


def compute_natal_sihua_layer(zwds: dict) -> dict:
    """
    Scan all 12 palaces for v2 Sihua fields and emit a structured layer.

    Returns:
      {
        "birth_year_findings": [{palace, star, type, weight}, ...],
        "self_hua_findings":   [{palace, star, type, weight}, ...],
        "flying_findings":     [{from_palace, to_palace, star, type, weight}, ...],
        "origin_palace":       "Career" | None,
        "has_v2_data":         bool,   # False if no v2 fields present anywhere
      }
    """
    palaces = zwds.get("palaces", [])
    if not isinstance(palaces, list):
        return _empty_layer()

    birth_year_findings = []
    self_hua_findings = []
    flying_findings = []
    has_any_v2 = False

    for p in palaces:
        palace_name = _get_palace_english(p)
        if not palace_name:
            continue

        # Birth-year Sihua on this palace
        for entry in _sihua_entries(p, "birth_year_sihua"):
            has_any_v2 = True
            birth_year_findings.append({
                "palace": palace_name,
                "star": entry.get("star", ""),
                "type": entry.get("type", ""),
                "weight": SIHUA_META.get(entry.get("type", ""), {}).get("weight", 0.2),
            })

        # 自化 on this palace
        for entry in _sihua_entries(p, "self_hua"):
            has_any_v2 = True
            self_hua_findings.append({
                "palace": palace_name,
                "star": entry.get("star", ""),
                "type": entry.get("type", ""),
                "weight": SIHUA_META.get(entry.get("type", ""), {}).get("weight", 0.2),
            })

        # Incoming flying Sihua (this palace is the target)
        for entry in _sihua_entries(p, "incoming_sihua"):
            has_any_v2 = True
            flying_findings.append({
                "from_palace": entry.get("from_palace", ""),
                "to_palace":   palace_name,
                "star":        entry.get("star", ""),
                "type":        entry.get("type", ""),
                "weight":      SIHUA_META.get(entry.get("type", ""), {}).get("weight", 0.2),
            })

    return {
        "birth_year_findings": birth_year_findings,
        "self_hua_findings":   self_hua_findings,
        "flying_findings":     flying_findings,
        "origin_palace":       zwds.get("origin_palace_english"),
        "has_v2_data":         has_any_v2,
    }


def _empty_layer() -> dict:
    return {
        "birth_year_findings": [],
        "self_hua_findings":   [],
        "flying_findings":     [],
        "origin_palace":       None,
        "has_v2_data":         False,
    }


def contribute_natal_sihua_scores(natal_layer: dict, domain_scores: dict) -> list:
    """
    Inject natal-Sihua findings as scoring contributions into domain_scores.
    Mutates domain_scores in place, appending to each domain's score and sources.

    Also returns a list of human-readable findings that can be surfaced in
    the reading output (the "Wealth receives 忌 from Fortune" sentences).
    """
    if not natal_layer.get("has_v2_data"):
        return []

    findings_text = []

    # ── Birth-year Sihua ────────────────────────────────────────────
    for f in natal_layer["birth_year_findings"]:
        palace = f["palace"]
        stype = f["type"]
        kws = PALACE_KEYWORDS.get(palace, [])
        w = f["weight"]
        for kw in kws:
            domain_scores[kw]["score"] += w * 0.8   # baseline natal marker, slightly lower
            domain_scores[kw]["sources"].append(f"natal_birth_{stype}_{palace}")
        findings_text.append({
            "layer":      "natal_birth_sihua",
            "palace":     palace,
            "star":       f["star"],
            "type":       stype,
            "description": _describe_birth_sihua(palace, f["star"], stype),
        })

    # ── 自化 (self-transformation / personality leak) ────────────────
    for f in natal_layer["self_hua_findings"]:
        palace = f["palace"]
        stype = f["type"]
        kws = PALACE_KEYWORDS.get(palace, [])
        # Self-hua is STRUCTURAL and constant — high weight; amplified for 忌
        w = f["weight"] * (1.4 if stype == "ji" else 1.1)
        for kw in kws:
            domain_scores[kw]["score"] += w
            domain_scores[kw]["sources"].append(f"natal_self_{stype}_{palace}")
        findings_text.append({
            "layer":      "natal_self_hua",
            "palace":     palace,
            "star":       f["star"],
            "type":       stype,
            "description": _describe_self_hua(palace, f["star"], stype),
        })

    # ── Flying Sihua (inter-palace cause-and-effect) ────────────────
    for f in natal_layer["flying_findings"]:
        src = f["from_palace"]
        dst = f["to_palace"]
        stype = f["type"]
        # Target palace keywords get the primary contribution
        dst_kws = PALACE_KEYWORDS.get(dst, [])
        src_kws = PALACE_KEYWORDS.get(src, [])
        w = f["weight"]
        for kw in dst_kws:
            domain_scores[kw]["score"] += w
            domain_scores[kw]["sources"].append(f"natal_flying_{stype}_{src}_to_{dst}")
        # Source palace gets a small echo (it's draining/channeling into target)
        for kw in src_kws:
            domain_scores[kw]["score"] += w * 0.35
            domain_scores[kw]["sources"].append(f"natal_flying_source_{src}")
        findings_text.append({
            "layer":       "natal_flying_sihua",
            "from_palace": src,
            "to_palace":   dst,
            "star":        f["star"],
            "type":        stype,
            "description": _describe_flying_sihua(src, dst, f["star"], stype),
        })

    # ── 来因宫 (origin palace — karmic root) ─────────────────────────
    origin = natal_layer.get("origin_palace")
    if origin:
        kws = PALACE_KEYWORDS.get(origin, [])
        for kw in kws:
            domain_scores[kw]["score"] += 0.15
            domain_scores[kw]["sources"].append(f"origin_palace_{origin}")
        findings_text.append({
            "layer":       "origin_palace",
            "palace":      origin,
            "description": f"{origin} is the karmic source palace — "
                           f"themes here radiate through the whole chart.",
        })

    return findings_text


# ─── Human-readable finding generators ──────────────────────────────
#
# These produce the sentences that will appear in readings. Keep them
# specific and mechanical — no Barnum statements.

def _describe_birth_sihua(palace: str, star: str, stype: str) -> str:
    action = SIHUA_META.get(stype, {}).get("action", "affects")
    return (f"Birth-year {stype}-transformation on {star} in {palace} "
            f"— baseline karmic marker that {action} this life domain.")


def _describe_self_hua(palace: str, star: str, stype: str) -> str:
    if stype == "ji":
        return (f"{palace} self-transforms 忌 on {star} — unconscious leak in this "
                f"domain; things drain here without external cause.")
    if stype == "lu":
        return (f"{palace} self-transforms 禄 on {star} — unconscious generosity/"
                f"outflow in this domain.")
    if stype == "quan":
        return (f"{palace} self-transforms 权 on {star} — unconscious drive to "
                f"push/control in this domain.")
    if stype == "ke":
        return (f"{palace} self-transforms 科 on {star} — unconscious visibility-"
                f"seeking in this domain.")
    return f"{palace} self-transforms {stype} on {star}."


def _describe_flying_sihua(src: str, dst: str, star: str, stype: str) -> str:
    action = SIHUA_META.get(stype, {}).get("action", "affects")
    if stype == "ji":
        return (f"{dst} receives 忌 from {src} via {star} — {src} palace's demands "
                f"structurally {action} {dst}.")
    if stype == "lu":
        return (f"{dst} receives 禄 from {src} via {star} — {src} palace's activity "
                f"channels flow into {dst}.")
    if stype == "quan":
        return (f"{dst} receives 权 from {src} via {star} — {src} palace "
                f"{action} action in {dst}.")
    if stype == "ke":
        return (f"{dst} receives 科 from {src} via {star} — {src} palace "
                f"{action} reputation in {dst}.")
    return f"{dst} receives {stype} from {src} via {star}."
