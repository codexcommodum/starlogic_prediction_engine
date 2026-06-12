"""Event-class detection from enriched ZWDS annual data.

Reads the additive fields the ZWDS engine emits per year (annual_wheel,
sihua_activations, romance_positions, convergences, active_decade) and
scores canonical event signatures by STAR ARCHETYPE x SIHUA TYPE x
ANNUAL ROLE — the year is themed by what ACTIVATES, not merely by which
natal palace the year branch lands on.

Calibrated against known-event chart histories. Key validated signatures:
  - transit lu/quan/ke charging an annual role = that life domain "opens"
  - >=2 charges into the SAME role in one year = event-grade signature
  - tian_liang + lu/quan in Wealth role = rescue money (insurance,
    inheritance, bailout) — tian_liang is the shelter/protection star
  - wen_chang/wen_qu + ke = honors/recognition; + ji = academic/document
    crisis
  - annual/decade ji striking a star that carries birth-year lu =
    禄逢冲破 "fortune meets its breaker" — collapse signature
  - decade stem == annual stem (one year per decade) = pivotal,
    hyper-activated year
  - tai_yang = father/authority figure; tai_yin = mother/daughter —
    multi-layer hits on these mark person-events
Degrades gracefully: with a legacy (un-enriched) payload every function
returns empty/zero and callers fall back to old behavior.
"""
from __future__ import annotations
from collections import defaultdict

# ── Role → event class ──────────────────────────────────────────────
ROLE_CLASS = {
    "Life": "identity", "Siblings": "siblings_allies", "Spouse": "partnership",
    "Children": "children", "Wealth": "wealth", "Health": "health",
    "Travel": "relocation_movement", "Friends": "network", "Career": "career",
    "Property": "home_property", "Fortune": "inner_life",
    "Parents": "parents_authority",
}

# ── Star archetypes (mains + the 18 aux the chart places) ───────────
STAR_ARCHETYPES = {
    "zi_wei":    "status, authority of the self, formal elevation",
    "tian_ji":   "pivot, strategy, change of direction",
    "tai_yang":  "father, male authority, public visibility",
    "wu_qu":     "money in motion, liquidity, decisive execution",
    "tian_tong": "ease, renewal, emotional contentment",
    "lian_zhen": "career fortune, passion, entanglement",
    "tian_fu":   "stored assets, stability, stewardship",
    "tai_yin":   "mother, daughters, quiet accumulation, real property",
    "tan_lang":  "desire, romance, appetite, speculation",
    "ju_men":    "speech, dispute, negotiation, rumor",
    "tian_xiang": "contracts, the seal, loyal support",
    "tian_liang": "shelter, insurance, rescue, elders, inheritance",
    "qi_sha":    "rupture, bold strike, leaving the old structure",
    "po_jun":    "breaking and rebuilding, uprooting, reinvention",
    "wen_chang": "scholarship, examinations, documents",
    "wen_qu":    "arts, eloquence, alternative learning",
    "zuo_fu":    "helpful allies, formalization, joining",
    "you_bi":    "supporters, assistance, seconding",
    "tian_kui":  "benefactor (yang), mentor's door",
    "tian_yue":  "benefactor (yin), quiet patronage",
    "lu_cun":    "salary, retained wealth, prudence",
    "qing_yang": "the blade, friction, surgical cuts",
    "tuo_luo":   "grinding delay, entanglement",
    "huo_xing":  "sudden fire, eruption, acceleration",
    "ling_xing": "slow burn, background alarm",
    "di_jie":    "emptying, plans dissolving",
    "di_kong":   "void, idealism over substance",
    "tian_ma":   "the post horse — movement, relocation, travel",
    "hong_luan": "red phoenix — marriage, romance bloom",
    "tian_xi":   "heavenly joy — celebration, births, weddings",
    "gu_chen":   "solitude (yang), going it alone",
    "gua_su":    "solitude (yin), separateness",
}

_CHARGE = ("lu", "quan", "ke")


def _edges(entry: dict):
    sa = entry.get("sihua_activations") or {}
    for layer in ("decade", "annual"):
        for e in sa.get(layer) or []:
            yield layer, e


def _birth_lu_stars(entry: dict) -> set:
    """Stars carrying birth-year Lu, read off the annual wheel."""
    out = set()
    for w in entry.get("annual_wheel") or []:
        for s in w.get("birth_year_sihua") or []:
            if s.get("type") == "lu":
                out.add(s.get("star"))
    return out


def compute_event_signals(entry: dict, age: int) -> dict:
    """Score event classes for one enriched annuals[] entry.

    Returns {"available", "classes", "is_pivotal", "activation_load",
    "top_class"}. With a legacy payload returns available=False.
    """
    if not entry or not entry.get("annual_wheel"):
        return {"available": False, "classes": [], "is_pivotal": False,
                "activation_load": 0.0, "top_class": None}

    charge = defaultdict(float)      # class -> opening/charge score
    strain = defaultdict(float)      # class -> pressure score
    evidence = defaultdict(list)
    role_charges = defaultdict(list)  # role -> [(layer, type, star)]

    # 1. Transit sihua into annual roles
    for layer, e in _edges(entry):
        role = (e.get("annual_role") or {}).get("role_english", "")
        cls = ROLE_CLASS.get(role)
        if not cls:
            continue
        star, typ = e.get("star", ""), e.get("type", "")
        arch = STAR_ARCHETYPES.get(star, star)
        if typ in _CHARGE:
            charge[cls] += 2.0
            role_charges[role].append((layer, typ, star))
            evidence[cls].append(f"{layer} {typ} on {star} ({arch}) in the year's {role} palace")
        elif typ == "ji":
            strain[cls] += 2.0
            evidence[cls].append(f"{layer} ji (knot/obstruction) on {star} ({arch}) in the year's {role} palace")

        # Natal-palace echo: the charged star also activates the life domain
        # of the NATAL palace it occupies (annual Siblings sitting on the
        # natal Wealth palace still reads as money). Half weight.
        natal_cls = ROLE_CLASS.get(e.get("natal_palace_english", ""))
        if natal_cls and natal_cls != cls:
            (charge if typ in _CHARGE else strain)[natal_cls] += 1.0
            evidence[natal_cls].append(
                f"{layer} {typ} on {star} ({arch}) — natal {e.get('natal_palace_english')} palace content activated")

        # Archetype star charged inside its matching role — strong kicker
        if typ in _CHARGE:
            if star == "tai_yin" and role == "Children":
                charge["children"] += 1.5
                evidence["children"].append("tai_yin (daughters) charged inside the year's Children palace")
            if star in ("hong_luan", "tian_xi") and role in ("Spouse", "Children"):
                charge["children" if role == "Children" else "partnership"] += 1.5

        # Archetype-specific boosts (calibrated)
        if star == "tian_liang" and typ in ("lu", "quan") and cls == "wealth":
            charge["windfall_rescue"] += 3.0
            evidence["windfall_rescue"].append(
                f"{layer} {typ} on tian_liang (shelter/insurance star) in the year's Wealth palace — rescue money signature")
        if star in ("wen_chang", "wen_qu"):
            if typ == "ke":
                charge["recognition"] += 2.5
                evidence["recognition"].append(f"{layer} ke on {star} — honors/examination success")
            elif typ == "ji":
                strain["recognition"] += 2.0
                evidence["recognition"].append(f"{layer} ji on {star} — academic/document crisis")
        if star == "tai_yang":
            charge["father_authority"] += 1.2
            evidence["father_authority"].append(f"{layer} {typ} on tai_yang (father/authority)")
        if star == "tai_yin":
            charge["mother_daughters"] += 1.2
            evidence["mother_daughters"].append(f"{layer} {typ} on tai_yin (mother/daughters)")
        if star == "wu_qu" and typ == "ji":
            strain["wealth"] += 1.5
            evidence["wealth"].append("ji on wu_qu — liquidity under pressure")

    # 2. Multi-charge bonus: >=2 charges into the same role in one year.
    # This is the calibrated event-grade signature — weight it decisively.
    for role, hits in role_charges.items():
        if len(hits) >= 2:
            cls = ROLE_CLASS[role]
            charge[cls] += 4.0
            evidence[cls].append(
                f"MULTI-CHARGE: {len(hits)} transformations converge on the year's {role} palace — event-grade signature")

    # 3. 禄逢冲破 — ji striking a birth-lu star
    birth_lu = _birth_lu_stars(entry)
    for layer, e in _edges(entry):
        if e.get("type") == "ji" and e.get("star") in birth_lu:
            role = (e.get("annual_role") or {}).get("role_english", "")
            cls = ROLE_CLASS.get(role, "wealth")
            strain[cls] += 3.0
            strain["wealth"] += 1.5
            evidence[cls].append(
                f"{layer} ji strikes {e.get('star')} which carries birth-year lu — 禄逢冲破, fortune meets its breaker (collapse signature)")

    # 4. Romance axis (age-gated)
    rp = entry.get("romance_positions") or {}
    if 18 <= age <= 55:
        for star, d in rp.items():
            role = (d.get("annual_role") or {}).get("role_english", "")
            if d.get("conjunct_annual_life") or role in ("Life", "Spouse"):
                charge["partnership"] += 1.5
                evidence["partnership"].append(
                    f"{star} ({STAR_ARCHETYPES.get(star, star)}) sits in the year's {role or 'Life'} palace")
                if role_charges.get("Spouse"):
                    charge["partnership"] += 1.5
                    evidence["partnership"].append("romance star + charged Spouse palace, same year")

    # 5. Convergences (multi-layer star pile-ups)
    for c in entry.get("convergences") or []:
        role = (c.get("annual_role") or {}).get("role_english", "")
        cls = ROLE_CLASS.get(role)
        if not cls:
            continue
        inten = float(c.get("intensity", 0) or 0)
        types = c.get("types") or []
        bucket = strain if all(t == "ji" for t in types) else charge
        bucket[cls] += inten / (2.0 if inten >= 5 else 3.0)
        evidence[cls].append(
            f"{'+'.join(c.get('layers', []))} converge on {c.get('star')} ({STAR_ARCHETYPES.get(c.get('star',''), '')}) in the year's {role} palace [{'+'.join(types)}] i={inten}")

    # 6. Year's Ming flavor (legacy technique, demoted to seasoning)
    ln_ming_natal = entry.get("palace_name_english", "")
    if ln_ming_natal in ROLE_CLASS:
        charge[ROLE_CLASS[ln_ming_natal]] += 1.0
        evidence[ROLE_CLASS[ln_ming_natal]].append(
            f"the year's Life palace sits on the natal {ln_ming_natal} palace")

    # 7. Pivotal years: decade stem == annual stem
    is_pivotal = False
    ad = entry.get("active_decade") or {}
    ysb = (entry.get("year_stem_branch") or "").split()
    if ad.get("palace_stem") and ysb and ad["palace_stem"] == ysb[0]:
        is_pivotal = True
        for cls in list(charge.keys()) or ["identity"]:
            charge[cls] += 0.5
        evidence["identity"].append(
            "decade stem and year stem coincide — once-per-decade hyper-activated year")

    # 7.5 Ambient-class haircut: identity/inner_life accumulate from every
    # year's wheel mechanics (Life/Fortune roles always exist) — they are
    # weather, not events. Demote so concrete event classes outrank them.
    for ambient in ("identity", "inner_life"):
        charge[ambient] *= 0.65
        strain[ambient] *= 0.65

    # 8. Age gating
    if age <= 12:
        for cls in ("partnership", "career", "wealth", "windfall_rescue"):
            charge[cls] *= 0.25
            strain[cls] *= 0.5
        for cls in ("parents_authority", "relocation_movement", "home_property"):
            charge[cls] *= 1.3   # childhood events arrive through the family
    if age < 16 or age > 58:
        charge["children"] *= 0.3

    # Assemble ranked classes
    classes = []
    for cls in set(list(charge.keys()) + list(strain.keys())):
        ch, st = round(charge[cls], 2), round(strain[cls], 2)
        total = ch + st
        if total < 1.0:
            continue
        direction = ("strained" if st > ch * 1.5 else
                     "charged" if ch > st * 1.5 else "volatile")
        classes.append({
            "class": cls, "score": round(total, 2),
            "charge": ch, "strain": st, "direction": direction,
            "evidence": evidence[cls][:5],
        })
    classes.sort(key=lambda c: -c["score"])

    activation_load = round(sum(c["score"] for c in classes), 2)
    return {
        "available": True,
        "classes": classes[:5],
        "is_pivotal": is_pivotal,
        "activation_load": activation_load,
        "top_class": classes[0]["class"] if classes else None,
    }


def flag_compression_years(all_years: list) -> None:
    """Relative, per-person compression: a year is a compression year only
    if its activation_load sits in the top ~18% of that person's lifetime
    distribution AND clears an absolute floor. Replaces the old absolute
    '3+ MEDIUM themes' rule, which static natal signatures satisfied every
    single year (the always-on badge bug). Mutates compression_year in place.
    Falls back silently if event signals are unavailable (legacy payload).
    """
    loads = [
        (y.get("event_signals") or {}).get("activation_load", 0.0)
        for y in all_years
        if (y.get("event_signals") or {}).get("available")
    ]
    if not loads or len(loads) < 10:
        return  # legacy payload — leave old flags untouched
    ranked = sorted(loads)
    p82 = ranked[int(len(ranked) * 0.82)]
    floor = 8.0
    threshold = max(floor, p82)
    for y in all_years:
        es = y.get("event_signals") or {}
        if es.get("available"):
            y["compression_year"] = es.get("activation_load", 0.0) >= threshold
