"""
bridge_format.py — Additive engine→frontend bridge.

The Base44 reading page binds to four top-level fields the reverted /reading
response no longer emitted. This module reshapes the EXISTING per-year signals
(all_years) into those four fields. It is pure Python, deterministic, adds zero
LLM calls, and never mutates the signals it reads.

Emitted fields (exact frontend contract):
    current_age        int
    year_narratives[]  {age, year, opportunities[], warnings[], compression_year, confidence}
    eras[]             {era_number, label, age_range:[s,e], tense,
                        top_themes[], compression_ages[], decade_transitions[], profection_arc[]}
    landmarks[]        {age, year, score, reasons[], tense, summary}

tense ∈ {"retrospective","current","predictive"} relative to current_age.
"""

from typing import List, Dict

_ORDINALS = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth",
             "Seventh", "Eighth", "Ninth", "Tenth", "Eleventh", "Twelfth"]

_CYCLE_LEN = 12  # one Hellenistic profection cycle = 12 years


# ─────────────────────────────────────────────
#  TENSE
# ─────────────────────────────────────────────

def _tense_range(start: int, end: int, current_age: int) -> str:
    if current_age is None:
        return "predictive"
    if current_age > end:
        return "retrospective"
    if current_age < start:
        return "predictive"
    return "current"


def _tense_point(age: int, current_age: int) -> str:
    if current_age is None:
        return "predictive"
    if age < current_age:
        return "retrospective"
    if age > current_age:
        return "predictive"
    return "current"


# ─────────────────────────────────────────────
#  YEAR NARRATIVES  (flat per-year array)
# ─────────────────────────────────────────────

def build_year_narratives_array(all_years: List[dict]) -> List[dict]:
    """Project each signals entry down to the fields the timeline binds to.
    opportunities/warnings are passed through untouched (already carry
    theme, confidence, headline, action, tone, evidence_keys)."""
    out = []
    for y in all_years:
        es = y.get("event_signals") or {}
        out.append({
            "age": y.get("age"),
            "year": y.get("year"),
            "opportunities": y.get("opportunities", []),
            "warnings": y.get("warnings", []),
            "compression_year": bool(y.get("compression_year", False)),
            "confidence": y.get("confidence", "NONE"),
            # Additive: ranked event classes from the activation layer
            "event_classes": [
                {"class": c.get("class"), "score": c.get("score"),
                 "direction": c.get("direction")}
                for c in (es.get("classes") or [])[:3]
            ],
            "is_pivotal": bool(es.get("is_pivotal", False)),
        })
    return out


# ─────────────────────────────────────────────
#  ERAS  (12-year profection cycles)
# ─────────────────────────────────────────────

def _era_label(idx_one_based: int) -> str:
    if idx_one_based <= len(_ORDINALS):
        return f"{_ORDINALS[idx_one_based - 1]} Profection Cycle"
    return f"Profection Cycle {idx_one_based}"


def build_eras(all_years: List[dict], current_age: int) -> List[dict]:
    if not all_years:
        return []
    by_age: Dict[int, dict] = {y["age"]: y for y in all_years if "age" in y}
    if not by_age:
        return []
    max_age = max(by_age)

    eras = []
    start = 0
    k = 0
    while start <= max_age:
        end = min(start + _CYCLE_LEN - 1, max_age)
        k += 1
        years = [by_age[a] for a in range(start, end + 1) if a in by_age]

        # Dominant themes: weight HIGH=2, MEDIUM=1, ignore LOW/NONE.
        theme_weight: Dict[str, int] = {}
        for y in years:
            for t in y.get("themes", []):
                c = t.get("confidence")
                if c == "HIGH":
                    theme_weight[t["theme"]] = theme_weight.get(t["theme"], 0) + 2
                elif c == "MEDIUM":
                    theme_weight[t["theme"]] = theme_weight.get(t["theme"], 0) + 1
        top_themes = [t for t, _ in sorted(theme_weight.items(), key=lambda x: -x[1])[:4]]

        compression_ages = [y["age"] for y in years if y.get("compression_year")]

        decade_transitions = []
        for y in years:
            dec = y.get("decade", {}) or {}
            if dec.get("position") == "TRANSITION_IN" and dec.get("palace_name"):
                decade_transitions.append(f"Age {y['age']}: enters {dec['palace_name']}")

        profection_arc = [(y.get("profection", {}) or {}).get("house") for y in years]

        eras.append({
            "era_number": k,
            "label": _era_label(k),
            "age_range": [start, end],
            "tense": _tense_range(start, end, current_age),
            "top_themes": top_themes,
            "compression_ages": compression_ages,
            "decade_transitions": decade_transitions,
            "profection_arc": profection_arc,
        })
        start = end + 1
    return eras


# ─────────────────────────────────────────────
#  LANDMARKS  (3-5 highest-convergence years)
# ─────────────────────────────────────────────

def _landmark_score(y: dict) -> float:
    conv = y.get("convergence", {}) or {}
    score = float(conv.get("high_confidence_count", 0) or 0)
    if y.get("compression_year"):
        score += 2.5
    high_themes = [t for t in y.get("themes", []) if t.get("confidence") == "HIGH"]
    score += 0.75 * len(high_themes)
    for d in conv.get("top_domains", []):
        if d.get("domain") in ("major_event", "major_transition") and d.get("confidence") == "HIGH":
            score += 1.5
            break
    # Event signals (star archetype x sihua x annual role) dominate when
    # available — they are the calibrated event-grade signatures.
    es = y.get("event_signals") or {}
    if es.get("available"):
        classes = es.get("classes") or []
        if classes:
            score += min(classes[0].get("score", 0.0), 10.0) * 0.8
        if es.get("is_pivotal"):
            score += 2.0
        if any("MULTI-CHARGE" in ev for c in classes for ev in c.get("evidence", [])):
            score += 2.0
        # Tiebreak: total activation load (prevents identical capped scores)
        score += min(es.get("activation_load", 0.0), 30.0) * 0.04
    return score


def _landmark_reasons(y: dict) -> List[str]:
    reasons = []
    # Event-signature evidence first — the most specific, calibrated layer.
    es = y.get("event_signals") or {}
    for c in (es.get("classes") or [])[:2]:
        label = c.get("class", "").replace("_", " ")
        reasons.append(f"{label} ({c.get('direction','')})")
        if c.get("evidence"):
            reasons.append(c["evidence"][0])
    if es.get("is_pivotal"):
        reasons.append("decade stem meets year stem — once-per-decade activation")
    conv = y.get("convergence", {}) or {}
    hc = conv.get("high_confidence_count", 0) or 0
    if y.get("compression_year"):
        reasons.append(f"compression year — {hc} stacked signals")
    elif hc:
        reasons.append(f"{hc} high-confidence convergence signals")
    for t in [t["theme"] for t in y.get("themes", []) if t.get("confidence") == "HIGH"][:3]:
        reasons.append(t.replace("_", " "))
    for d in conv.get("top_domains", []):
        if d.get("domain") == "major_event" and d.get("confidence") == "HIGH":
            reasons.append("defining aspect to the sect light")
            break
    if not reasons:
        reasons.append("notable convergence")
    seen, out = set(), []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def build_landmarks(all_years: List[dict], current_age: int,
                    min_n: int = 3, max_n: int = 5) -> List[dict]:
    # Exclude age 0 (birth) from landmark consideration.
    candidates = [y for y in all_years if (y.get("age") or 0) >= 1]
    scored = sorted(((y, _landmark_score(y)) for y in candidates), key=lambda x: -x[1])
    chosen = [pair for pair in scored if pair[1] > 0][:max_n]
    if len(chosen) < min_n:
        chosen = scored[:min_n]

    # De-dup by age, then present in timeline (age-ascending) order.
    dedup = {}
    for y, sc in chosen:
        dedup[y["age"]] = (y, sc)
    ordered = sorted(dedup.values(), key=lambda x: x[0]["age"])

    out = []
    for y, sc in ordered:
        es = y.get("event_signals") or {}
        es_classes = [c.get("class", "").replace("_", " ")
                      for c in (es.get("classes") or [])[:2]]
        themes = [t["theme"].replace("_", " ")
                  for t in y.get("themes", [])
                  if t.get("confidence") in ("HIGH", "MEDIUM")][:2]
        lead = es_classes or themes
        summary = f"Age {y['age']} ({y['year']}): " + (", ".join(lead) if lead else "a defining year")
        out.append({
            "age": y["age"],
            "year": y["year"],
            "score": round(sc, 2),
            "reasons": _landmark_reasons(y),
            "tense": _tense_point(y["age"], current_age),
            "summary": summary,
        })
    return out
