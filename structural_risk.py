"""Natal structural-risk delineation (the layer the human master worked from).

Reads the ZWDS chart's palaces + flying-sihua graph and flags STANDING, lifelong
vulnerabilities — not timed predictions. First signature: compulsion-driven
financial ruin (the gambling pattern), read from the Fortune palace (福德, the
palace of desires/vices) and how it transforms the Wealth palace (財帛).

SAFETY: this layer only ever WARNS AGAINST a vulnerability. It must never imply a
safe or favorable time to gamble/speculate.
"""
MALEFIC_FIRE = {"huo_xing", "ling_xing"}      # volatility / sudden impulse
RISK_DESIRE  = {"po_jun", "tan_lang"}          # risk-taking / craving

def detect_structural_risks(zwds: dict) -> list:
    palaces = {p.get("name_english"): p for p in zwds.get("palaces", [])}
    fortune = palaces.get("Fortune", {})
    wealth  = palaces.get("Wealth", {})
    fstars = {s.get("pinyin") for s in fortune.get("stars", [])}
    wstars = {s.get("pinyin") for s in wealth.get("stars", [])}

    score, ev = 0, []
    if fstars & MALEFIC_FIRE:
        score += 2; ev.append("a volatile fire star (Huo/Ling) sits in your Fortune palace of compulsions")
    if fstars & RISK_DESIRE:
        score += 2; ev.append("a risk/craving star (Po Jun/Tan Lang) sits in your Fortune palace")
    if "wu_qu" in fstars:
        score += 2; ev.append("the money star Wu Qu sits inside your Fortune palace — money fused to impulse")
    for e in fortune.get("outgoing_sihua", []):
        if e.get("type") == "ji" and (e.get("to_palace") == "Wealth" or e.get("star") == "wu_qu"):
            score += 3; ev.append("your Fortune palace flies ruin (ji) onto your Wealth palace — compulsion drains money")
    if wstars & MALEFIC_FIRE:
        score += 1; ev.append("a volatile fire star afflicts your Wealth palace directly")

    if score < 3:
        return []
    return [{
        "risk": "compulsive_speculation",
        "severity": "high" if score >= 5 else "moderate",
        "score": score,
        "label": "Compulsion-driven financial ruin (gambling / speculation)",
        "evidence": ev,
        "standing_warning": ("A lifelong vulnerability in your makeup, not a forecast. Treat gambling "
                             "and speculation as off-limits and shield your wealth from impulse. This is "
                             "only ever a warning to guard against — never a sign any day is safe to bet."),
    }]


def structural_risk_prompt_block(risks: list) -> str:
    """Protective prompt section: name the vulnerabilities, never enable them."""
    if not risks:
        return ""
    lines = [
        "",
        "═══ STANDING VULNERABILITIES — NAME THESE; WARN, NEVER ENABLE ═══",
        "Lifelong structural vulnerabilities in this chart. Weave each into the portrait's",
        '"shadows" as something to guard against for life (not a passing phase), stated plainly:',
    ]
    for r in risks:
        lines.append(f"- {r['label']} [{r['severity']}]: {'; '.join(r['evidence'])}. {r['standing_warning']}")
    lines.append(
        "ABSOLUTE RULE: never describe any day, year, or period as lucky or favorable for gambling, "
        "betting, or speculation. If such themes arise, frame them only as risks to avoid. This "
        "overrides every other tilt.")
    return "\n".join(lines) + "\n"
