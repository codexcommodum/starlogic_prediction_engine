"""
narrative_bridge.py — Structured opportunity/warning entries from themes + convergence.

Architecture note (matches main.py):
    Engine produces structured data. Base44 InvokeLLM renders prose.
    This module is pure Python, deterministic, and adds zero LLM calls at runtime.

Inputs:
    themes      — list from theme_bridge.build_year_themes() (theme + confidence + sihua + evidence)
    convergence — dict from main.score_convergence() (top_domains + high_confidence_count + flags)
    year_data   — current year's full payload (profection, annual, decade, age)

Output:
    {
      "opportunities": [<entry>, ...],
      "warnings":      [<entry>, ...]
    }

Each <entry> shape:
    {
      "theme": str,
      "kind": "opportunity" | "warning",
      "confidence": "HIGH" | "MEDIUM",
      "valence": "favorable" | "forceful" | "visible" | "neutral" | "obstructed" | "convergence",
      "headline": str,                      # one-line, deterministic, ready for LLM
      "action": str,                        # imperative directive
      "tone": str,                          # decisive | gentle | strategic | watchful | neutral
      "evidence_keys": list[str],           # 2-4 short evidence strings carried from theme layer
      "context": dict,                      # year context the LLM may inline
      "compression_year": bool (optional)
    }

LOW-confidence themes are dropped to avoid noise.
"""

import re
from typing import Optional


# ─────────────────────────────────────────────
#  ROUTING
# ─────────────────────────────────────────────

OPPORTUNITY_VALENCES = {"favorable", "forceful", "visible", "neutral"}
WARNING_VALENCES = {"obstructed"}

SIHUA_TO_VALENCE = {
    "lu":   "favorable",
    "quan": "forceful",
    "ke":   "visible",
    "ji":   "obstructed",
}

DIGNITY_TO_VALENCE = {
    "exaltation": "favorable",
    "domicile":   "favorable",
    "peregrine":  "neutral",
    "fall":       "obstructed",
    "detriment":  "obstructed",
}


# ─────────────────────────────────────────────
#  AGE BRACKET LABELS — used by templates that mention life stage
# ─────────────────────────────────────────────

def _age_bracket(age: int) -> str:
    if age <= 13:  return "child"
    if age <= 17:  return "teen"
    if age <= 64:  return "adult"
    return "senior"


# ─────────────────────────────────────────────
#  TEMPLATES — 12 themes × 5 valences
#  Headlines are short, declarative, no mystical hedging.
#  Actions are imperative — Base44 LLM may soften, never hedge harder.
#  Placeholders: {time_lord} {dignity} {primary_house} {annual_palace}
#                {da_xian_palace} {age_bracket} {sihua_flavor}
# ─────────────────────────────────────────────

TEMPLATES = {
    # ── partnership ──────────────────────────
    ("partnership", "favorable"): {
        "headline": "Partnership channels open under {time_lord}",
        "action":   "Move on aligned offers — the year supports binding",
        "tone":     "decisive",
    },
    ("partnership", "forceful"): {
        "headline": "Partnership demands a decisive choice",
        "action":   "Pick the direction; half-measures get punished here",
        "tone":     "decisive",
    },
    ("partnership", "visible"): {
        "headline": "Partnership comes into public view",
        "action":   "Be intentional — others are watching the relationship form",
        "tone":     "strategic",
    },
    ("partnership", "neutral"): {
        "headline": "Partnership themes active this year",
        "action":   "Tend existing bonds; vet new ones before committing",
        "tone":     "neutral",
    },
    ("partnership", "obstructed"): {
        "headline": "Partnership friction; signals don't add up",
        "action":   "Pause new commitments — clarify intentions before signing",
        "tone":     "watchful",
    },

    # ── wealth_gain ──────────────────────────
    ("wealth_gain", "favorable"): {
        "headline": "Income flow opens through {time_lord}",
        "action":   "Position for growth — the lord delivers from H{primary_house}",
        "tone":     "decisive",
    },
    ("wealth_gain", "forceful"): {
        "headline": "Money decisions can't wait",
        "action":   "Negotiate hard — the year rewards directness, not patience",
        "tone":     "decisive",
    },
    ("wealth_gain", "visible"): {
        "headline": "Financial standing becomes public",
        "action":   "Audit the numbers — reputation precedes the deal this year",
        "tone":     "strategic",
    },
    ("wealth_gain", "neutral"): {
        "headline": "Wealth themes active under {da_xian_palace}",
        "action":   "Steady accumulation favored; postpone speculation",
        "tone":     "neutral",
    },
    ("wealth_gain", "obstructed"): {
        "headline": "Income friction; flow gets blocked",
        "action":   "Defend reserves — postpone large outlays until pressure clears",
        "tone":     "watchful",
    },

    # ── property_home ────────────────────────
    ("property_home", "favorable"): {
        "headline": "Home and property settle into place",
        "action":   "Buy, plant, build — the foundation is supported now",
        "tone":     "decisive",
    },
    ("property_home", "forceful"): {
        "headline": "Property decisions force themselves",
        "action":   "Move on the move — staying static costs more than acting",
        "tone":     "decisive",
    },
    ("property_home", "visible"): {
        "headline": "Home becomes the public stage",
        "action":   "Hosting and visibility align; choose the moment deliberately",
        "tone":     "strategic",
    },
    ("property_home", "neutral"): {
        "headline": "Home themes active in {annual_palace}",
        "action":   "Tend foundation; defer cosmetic projects this year",
        "tone":     "neutral",
    },
    ("property_home", "obstructed"): {
        "headline": "Home pressure surfaces",
        "action":   "Don't sign property paperwork yet — friction hides flaws",
        "tone":     "watchful",
    },

    # ── career_pivot ─────────────────────────
    ("career_pivot", "favorable"): {
        "headline": "Career path opens cleanly",
        "action":   "Take the role — {time_lord} backs the change",
        "tone":     "decisive",
    },
    ("career_pivot", "forceful"): {
        "headline": "Career demands a hard pivot",
        "action":   "Pick the lane and commit; dilution costs more than focus",
        "tone":     "decisive",
    },
    ("career_pivot", "visible"): {
        "headline": "Work output gets recognized",
        "action":   "Polish the public-facing work — judgment is happening",
        "tone":     "strategic",
    },
    ("career_pivot", "neutral"): {
        "headline": "Career themes active this year",
        "action":   "Build skill, hold position; the right move is later, not now",
        "tone":     "neutral",
    },
    ("career_pivot", "obstructed"): {
        "headline": "Career friction blocks momentum",
        "action":   "Pause big moves — the current plan has hidden cost",
        "tone":     "watchful",
    },

    # ── health_event ─────────────────────────
    ("health_event", "favorable"): {
        "headline": "Vitality and recovery favored",
        "action":   "Address chronic items now — the body cooperates this year",
        "tone":     "decisive",
    },
    ("health_event", "forceful"): {
        "headline": "Health demands attention",
        "action":   "Get the test, change the habit — don't defer",
        "tone":     "decisive",
    },
    ("health_event", "visible"): {
        "headline": "Body becomes a public concern",
        "action":   "Be transparent with care providers; precision matters",
        "tone":     "strategic",
    },
    ("health_event", "neutral"): {
        "headline": "Health themes active in {annual_palace}",
        "action":   "Maintain rhythm; small adjustments compound over the year",
        "tone":     "neutral",
    },
    ("health_event", "obstructed"): {
        "headline": "Health pressure on body palace",
        "action":   "Preventive checkups, lower stress load — don't push through",
        "tone":     "watchful",
    },

    # ── uprooting_travel ─────────────────────
    ("uprooting_travel", "favorable"): {
        "headline": "Movement opens new ground",
        "action":   "Take the trip, take the offer — relocation favored",
        "tone":     "decisive",
    },
    ("uprooting_travel", "forceful"): {
        "headline": "Travel or relocation forces a choice",
        "action":   "Decide direction; drifting costs more than committing",
        "tone":     "decisive",
    },
    ("uprooting_travel", "visible"): {
        "headline": "Public movement and exposure",
        "action":   "Travel is observed — pick destinations with purpose",
        "tone":     "strategic",
    },
    ("uprooting_travel", "neutral"): {
        "headline": "Travel themes active this year",
        "action":   "Plan trips with intention; logistics matter more than usual",
        "tone":     "neutral",
    },
    ("uprooting_travel", "obstructed"): {
        "headline": "Travel and movement get tangled",
        "action":   "Build slack into plans — friction shows up in transit",
        "tone":     "watchful",
    },

    # ── friends_network ──────────────────────
    ("friends_network", "favorable"): {
        "headline": "Network expands toward you",
        "action":   "Say yes to introductions — {time_lord} is connecting",
        "tone":     "decisive",
    },
    ("friends_network", "forceful"): {
        "headline": "Network demands you lead",
        "action":   "Step into the convener role; people are waiting for it",
        "tone":     "decisive",
    },
    ("friends_network", "visible"): {
        "headline": "Reputation in the network rises",
        "action":   "Show up consistently — trust compounds publicly this year",
        "tone":     "strategic",
    },
    ("friends_network", "neutral"): {
        "headline": "Friend themes active this year",
        "action":   "Tend existing alliances; depth beats reach now",
        "tone":     "neutral",
    },
    ("friends_network", "obstructed"): {
        "headline": "Friend network friction",
        "action":   "Don't lend your reputation — vet new entrants carefully",
        "tone":     "watchful",
    },

    # ── transformation_loss ──────────────────
    ("transformation_loss", "favorable"): {
        "headline": "Release clears space for what's coming",
        "action":   "Let go cleanly — the new path needs the room",
        "tone":     "gentle",
    },
    ("transformation_loss", "forceful"): {
        "headline": "Transformation can't be deferred",
        "action":   "Cut what's dead; half-cuts heal slowly",
        "tone":     "decisive",
    },
    ("transformation_loss", "visible"): {
        "headline": "Transformation happens in public view",
        "action":   "Own the change publicly — hiding it costs more",
        "tone":     "strategic",
    },
    ("transformation_loss", "neutral"): {
        "headline": "Transformation themes active under {da_xian_palace}",
        "action":   "Let small endings happen; resist nothing this year",
        "tone":     "gentle",
    },
    ("transformation_loss", "obstructed"): {
        "headline": "Loss pressure builds; the impulse is to cling",
        "action":   "Grieve actively — denial extends the wound",
        "tone":     "watchful",
    },

    # ── family_parents ───────────────────────
    ("family_parents", "favorable"): {
        "headline": "Family lines warm and reconnect",
        "action":   "Make the call — repair work is supported now",
        "tone":     "gentle",
    },
    ("family_parents", "forceful"): {
        "headline": "Family role demands you step up",
        "action":   "Take responsibility; passing it costs the line",
        "tone":     "decisive",
    },
    ("family_parents", "visible"): {
        "headline": "Family standing becomes visible",
        "action":   "Honor the elders publicly — it's witnessed",
        "tone":     "strategic",
    },
    ("family_parents", "neutral"): {
        "headline": "Family themes active this year",
        "action":   "Show up steady; presence matters more than gestures",
        "tone":     "neutral",
    },
    ("family_parents", "obstructed"): {
        "headline": "Family friction surfaces",
        "action":   "Hold boundaries with love — not all asks are yours to meet",
        "tone":     "watchful",
    },

    # ── creative_children ────────────────────
    ("creative_children", "favorable"): {
        "headline": "Creation and children flow open",
        "action":   "Birth the project, the child, the work — alignment is real",
        "tone":     "decisive",
    },
    ("creative_children", "forceful"): {
        "headline": "Creative work demands you ship",
        "action":   "Stop iterating — release and let it land",
        "tone":     "decisive",
    },
    ("creative_children", "visible"): {
        "headline": "Creative output gets seen",
        "action":   "Polish the front-facing; viewers are arriving",
        "tone":     "strategic",
    },
    ("creative_children", "neutral"): {
        "headline": "Creative themes active under {time_lord}",
        "action":   "Daily practice; the work compounds quietly this year",
        "tone":     "neutral",
    },
    ("creative_children", "obstructed"): {
        "headline": "Creative blocks; output stalls",
        "action":   "Step back — forcing it makes worse work",
        "tone":     "watchful",
    },

    # ── identity_self ────────────────────────
    ("identity_self", "favorable"): {
        "headline": "Self comes into clear focus",
        "action":   "Claim the new identity — the year supports the becoming",
        "tone":     "decisive",
    },
    ("identity_self", "forceful"): {
        "headline": "Identity demands a stand",
        "action":   "Pick the line and hold it; ambivalence costs the most",
        "tone":     "decisive",
    },
    ("identity_self", "visible"): {
        "headline": "Self enters public spotlight",
        "action":   "Be deliberate — your image is being formed in real time",
        "tone":     "strategic",
    },
    ("identity_self", "neutral"): {
        "headline": "Self themes active this year",
        "action":   "Quiet self-work; reorganize internally before announcing",
        "tone":     "neutral",
    },
    ("identity_self", "obstructed"): {
        "headline": "Identity friction; the old self resists",
        "action":   "Don't fight the molt — let the old skin go slowly",
        "tone":     "gentle",
    },

    # ── hidden_endings ───────────────────────
    ("hidden_endings", "favorable"): {
        "headline": "Quiet endings clear hidden weight",
        "action":   "Close it without ceremony — completion is the gift",
        "tone":     "gentle",
    },
    ("hidden_endings", "forceful"): {
        "headline": "Hidden matters force resolution",
        "action":   "Surface what's buried; partial truths cost the most",
        "tone":     "decisive",
    },
    ("hidden_endings", "visible"): {
        "headline": "Hidden things come to light",
        "action":   "Lead the disclosure — discovery hurts more than confession",
        "tone":     "strategic",
    },
    ("hidden_endings", "neutral"): {
        "headline": "Endings themes active this year",
        "action":   "Tend closures, files, debts; tie loose ends",
        "tone":     "neutral",
    },
    ("hidden_endings", "obstructed"): {
        "headline": "Hidden pressure compounds underneath",
        "action":   "Don't ignore the quiet drain — name it before it leaks",
        "tone":     "watchful",
    },
}


# ─────────────────────────────────────────────
#  CONVERGENCE FALLBACKS
#  Fire only when no theme produced an entry of the matching kind.
#  Pulls from score_convergence() top_domains.
# ─────────────────────────────────────────────

CONVERGENCE_FALLBACK = {
    # opportunity-side
    "support_arriving": {
        "headline": "Support arrives this year",
        "action":   "Open hand, don't grasp — reception matters more than chase",
        "tone":     "gentle",
    },
    "major_event": {
        "headline": "Tight aspect to sect light: a defining moment",
        "action":   "Pay attention to the inflection — it's marking time",
        "tone":     "strategic",
    },
    "resilience": {
        "headline": "Inner ground holds steady this year",
        "action":   "Lean on it — others may need to borrow your steadiness",
        "tone":     "neutral",
    },
    # warning-side
    "crisis_pressure": {
        "headline": "Hard aspect activated — pressure tests structure",
        "action":   "Reinforce foundations; don't add load this year",
        "tone":     "watchful",
    },
    "pressure": {
        "headline": "Background pressure on identity and form",
        "action":   "Keep the nervous system steady; sleep, water, repeat",
        "tone":     "watchful",
    },
    "major_transition": {
        "headline": "Cycle reset; the next decade begins forming",
        "action":   "Don't lock new commitments until the dust settles",
        "tone":     "strategic",
    },
}

OPPORTUNITY_FALLBACK_KEYS = ("support_arriving", "major_event", "resilience")
WARNING_FALLBACK_KEYS     = ("crisis_pressure", "pressure", "major_transition")


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

_PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

def _safe_format(template_str: str, ctx: dict) -> str:
    """Format with context; if a key is missing, drop the placeholder cleanly."""
    try:
        return template_str.format(**ctx)
    except (KeyError, IndexError):
        cleaned = _PLACEHOLDER_RE.sub("", template_str)
        return re.sub(r"\s{2,}", " ", cleaned).strip(" ,;.")


def _resolve_valence(theme_entry: dict, prof: dict) -> str:
    """
    Sihua wins if present (it's the most specific signal).
    Fall back to dignity. Default neutral.
    """
    sihua = theme_entry.get("sihua") or []
    if sihua:
        v = sihua[0].get("type", "")
        return SIHUA_TO_VALENCE.get(v, "neutral")
    dig = (prof.get("lord_dignity") or "peregrine").lower()
    return DIGNITY_TO_VALENCE.get(dig, "neutral")


def _build_context(year_data: dict) -> dict:
    prof = year_data.get("profection", {}) or {}
    annual = year_data.get("annual", {}) or {}
    decade = year_data.get("decade", {}) or {}
    age = year_data.get("age", 0)
    return {
        "time_lord":      prof.get("lord", "") or "",
        "dignity":        prof.get("lord_dignity", "peregrine") or "peregrine",
        "primary_house":  prof.get("house", "") or "",
        "lord_house":     prof.get("lord_house", "") or "",
        "annual_palace":  annual.get("palace_name", "") or "",
        "da_xian_palace": decade.get("palace_name", "") or "",
        "age":            age,
        "age_bracket":    _age_bracket(age),
    }


def _trim_evidence(theme_entry: dict, max_keys: int = 4) -> list:
    zwds_ev = theme_entry.get("zwds_evidence", []) or []
    hel_ev  = theme_entry.get("hellenistic_evidence", []) or []
    # Take the strongest (first) entries from each side
    return (zwds_ev[:2] + hel_ev[:2])[:max_keys]


# ─────────────────────────────────────────────
#  PUBLIC ENTRY POINT
# ─────────────────────────────────────────────

def build_year_narratives(themes: list,
                          convergence: dict,
                          year_data: dict) -> dict:
    """
    Produce structured opportunity/warning entries for a single year.

    Returns:
        {"opportunities": [...], "warnings": [...]}
    """
    ctx = _build_context(year_data)
    prof = year_data.get("profection", {}) or {}
    compression = bool(year_data.get("compression_year", False))

    opportunities = []
    warnings = []
    theme_emitted_opportunity = False
    theme_emitted_warning = False

    # ── Layer 1: theme-driven entries ─────────
    for t in (themes or []):
        if t.get("confidence") == "LOW":
            continue
        valence = _resolve_valence(t, prof)
        template = TEMPLATES.get((t["theme"], valence))
        if not template:
            continue

        kind = "opportunity" if valence in OPPORTUNITY_VALENCES else "warning"

        # If sihua present, surface its flavor in context (templates can use it)
        sihua_flavor = ""
        if t.get("sihua"):
            sihua_flavor = t["sihua"][0].get("flavor", "") or ""
        ctx_with_sihua = {**ctx, "sihua_flavor": sihua_flavor}

        entry = {
            "theme":         t["theme"],
            "kind":          kind,
            "confidence":    t.get("confidence", "MEDIUM"),
            "valence":       valence,
            "headline":      _safe_format(template["headline"], ctx_with_sihua),
            "action":        _safe_format(template["action"], ctx_with_sihua),
            "tone":          template.get("tone", "neutral"),
            "evidence_keys": _trim_evidence(t),
            "context":       ctx,
        }
        if compression:
            entry["compression_year"] = True

        if kind == "opportunity":
            opportunities.append(entry)
            theme_emitted_opportunity = True
        else:
            warnings.append(entry)
            theme_emitted_warning = True

    # ── Layer 2: convergence-domain fallbacks ─
    top_domains = convergence.get("top_domains", []) if convergence else []
    high_domains = {d["domain"]: d for d in top_domains
                    if d.get("confidence") == "HIGH"}

    if not theme_emitted_opportunity:
        for key in OPPORTUNITY_FALLBACK_KEYS:
            if key in high_domains:
                fb = CONVERGENCE_FALLBACK[key]
                entry = {
                    "theme":         key,
                    "kind":          "opportunity",
                    "confidence":    high_domains[key]["confidence"],
                    "valence":       "convergence",
                    "headline":      _safe_format(fb["headline"], ctx),
                    "action":        _safe_format(fb["action"], ctx),
                    "tone":          fb.get("tone", "neutral"),
                    "evidence_keys": [f"convergence:{key}"],
                    "context":       ctx,
                }
                if compression:
                    entry["compression_year"] = True
                opportunities.append(entry)
                break  # one fallback is enough

    if not theme_emitted_warning:
        for key in WARNING_FALLBACK_KEYS:
            if key in high_domains:
                fb = CONVERGENCE_FALLBACK[key]
                entry = {
                    "theme":         key,
                    "kind":          "warning",
                    "confidence":    high_domains[key]["confidence"],
                    "valence":       "convergence",
                    "headline":      _safe_format(fb["headline"], ctx),
                    "action":        _safe_format(fb["action"], ctx),
                    "tone":          fb.get("tone", "watchful"),
                    "evidence_keys": [f"convergence:{key}"],
                    "context":       ctx,
                }
                if compression:
                    entry["compression_year"] = True
                warnings.append(entry)
                break

    # ── Sort: HIGH first, MEDIUM after; preserve insertion order within ranks
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    opportunities.sort(key=lambda x: rank.get(x["confidence"], 9))
    warnings.sort(key=lambda x: rank.get(x["confidence"], 9))

    return {
        "opportunities": opportunities,
        "warnings":      warnings,
    }
