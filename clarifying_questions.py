"""
Starlogic — Clarifying Questions Generator (v2 — plain English)
Inspects a chart and generates 9 tailored True/False questions across 3 tiers:
  Tier 1 (Nayin + Sect): how the operating system runs
  Tier 2 (Hellenistic): how planets deliver
  Tier 3 (ZWDS stars): how stars manifest

All statements rewritten in plain English — no astrological jargon in user-visible text.
Universal: every branch covers a chart category, not a specific person.
"""

# ═══════════════════════════════════════════════════════════
# NAYIN CATEGORIZATION
# ═══════════════════════════════════════════════════════════

NAYIN_VISIBILITY_HIDDEN = {
    "hai_zhong_jin", "sha_zhong_jin", "jian_xia_shui", "lu_zhong_huo",
    "shan_xia_huo", "fu_deng_huo",
}
NAYIN_VISIBILITY_EXPOSED = {
    "jian_feng_jin", "shan_tou_huo", "pi_li_huo", "tian_shang_huo",
    "da_lin_mu", "chang_liu_shui", "da_xi_shui", "tian_he_shui",
    "da_hai_shui", "wu_shang_tu",
}
NAYIN_STRENGTH_ENDURING = {
    "hai_zhong_jin", "da_lin_mu", "song_bai_mu", "da_yi_tu",
    "da_hai_shui", "tian_he_shui",
}
NAYIN_STRENGTH_ADAPTIVE = {
    "yang_liu_mu", "bai_la_jin", "chang_liu_shui", "sang_zhe_mu",
    "ping_di_mu", "jian_xia_shui",
}


# ═══════════════════════════════════════════════════════════
# STAR CATEGORIZATION
# ═══════════════════════════════════════════════════════════

ZIWEI_GROUP = {"zi_wei", "tian_ji", "tai_yang", "wu_qu", "tian_tong", "lian_zhen"}
TIANFU_GROUP = {"tian_fu", "tai_yin", "tan_lang", "ju_men", "tian_xiang",
                "tian_liang", "qi_sha", "po_jun"}


# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════

def find_star_palace(zwds_palaces: list, target_star: str) -> str:
    for p in zwds_palaces:
        stars = p.get("stars", [])
        if isinstance(stars, list):
            for s in stars:
                pinyin = s.get("pinyin", "") if isinstance(s, dict) else str(s)
                if pinyin == target_star:
                    return p.get("name_english", "")
    return ""


def find_palace_stars(zwds_palaces: list, target_palace: str) -> list:
    for p in zwds_palaces:
        if p.get("name_english") == target_palace:
            stars = p.get("stars", [])
            if isinstance(stars, list):
                return [s.get("pinyin", "") if isinstance(s, dict) else str(s)
                        for s in stars]
    return []


# ═══════════════════════════════════════════════════════════
# TIER 1: NAYIN + SECT (Foundation)
# ═══════════════════════════════════════════════════════════

def q1_nayin_visibility(nayin_data: dict) -> dict:
    pinyin = nayin_data.get("pinyin", "")

    if pinyin in NAYIN_VISIBILITY_HIDDEN:
        statement = ("Your life builds quietly, out of sight, for years before people notice. "
                     "TRUE: I'm okay with that. I can work for a long time without recognition. "
                     "FALSE: I want visible progress now. Slow, invisible work frustrates me.")
    elif pinyin in NAYIN_VISIBILITY_EXPOSED:
        statement = ("Your life operates in the open. What you do is visible from the start. "
                     "TRUE: I do my best work when people can see it. I need a stage. "
                     "FALSE: I prefer working behind the scenes. Being visible drains me.")
    else:
        statement = ("Your life has both visible and hidden phases. "
                     "TRUE: I want progress I can show people. "
                     "FALSE: I'd rather do long, quiet work that pays off later.")

    return {
        "id": "q1_nayin_visibility",
        "tier": 1,
        "fork": "visibility",
        "statement": statement,
        "impact": "If TRUE: interpret toward public-facing outcomes (recognition, visible milestones). If FALSE: interpret toward long compound arcs, late-blooming wins.",
    }


def q2_nayin_strength(nayin_data: dict) -> dict:
    pinyin = nayin_data.get("pinyin", "")

    if pinyin in NAYIN_STRENGTH_ENDURING:
        statement = ("When life breaks you, you take the hit fully - and take a long time to rebuild. "
                     "TRUE: Setbacks cut deep. I don't bounce back fast, but when I come back I'm stronger than before. "
                     "FALSE: I move on quickly from setbacks. I don't dwell.")
    elif pinyin in NAYIN_STRENGTH_ADAPTIVE:
        statement = ("You adapt and reshape yourself when life pressures you, rather than holding your ground. "
                     "TRUE: I change direction easily. I don't stay attached to old plans that stop working. "
                     "FALSE: Once I commit to a path, I stick with it even when it stops working.")
    else:
        statement = ("How you handle pressure shapes how your life unfolds. "
                     "TRUE: I adapt and move. I reshape as needed. "
                     "FALSE: I hold ground. I wait it out.")

    return {
        "id": "q2_nayin_strength",
        "tier": 1,
        "fork": "strength",
        "statement": statement,
        "impact": "If TRUE (adaptive): predict pivots, resets, new beginnings after setbacks. If FALSE (enduring): predict long single arcs with deep recovery periods.",
    }


def q3_sect_condition(hellenistic: dict) -> dict:
    sect = hellenistic.get("sect", "unknown")

    if sect == "day":
        statement = ("You were born during the day. Your chart is wired for action, visibility, and outward movement. "
                     "TRUE: I come alive taking charge, being seen, and doing things in the world. "
                     "FALSE: Constant visibility drains me. I need privacy to recharge.")
    elif sect == "night":
        statement = ("You were born at night. Your chart is wired for intuition, emotional depth, and inward work. "
                     "TRUE: I come alive in reflective, emotionally connected spaces. "
                     "FALSE: I'd rather be doing something visible than sitting with my feelings.")
    else:
        statement = ("How you engage with the world shapes how your chart expresses. "
                     "TRUE: I run on intuition and emotional reading of situations. "
                     "FALSE: I run on logic and external achievement.")

    return {
        "id": "q3_sect_condition",
        "tier": 1,
        "fork": "sect_alignment",
        "statement": statement,
        "impact": "If TRUE: sect light is actively running - predict its domain strongly. If FALSE: sect light dormant, its natal house themes underactive.",
    }


# ═══════════════════════════════════════════════════════════
# TIER 2: HELLENISTIC (Planetary Delivery)
# ═══════════════════════════════════════════════════════════

def q4_benefic_expression(hellenistic: dict) -> dict:
    sect = hellenistic.get("sect", "night")
    benefic = "Jupiter" if sect == "day" else "Venus"

    planets = hellenistic.get("planets", [])
    benefic_dignity = "peregrine"
    for p in planets:
        if p.get("name", "").lower() == benefic.lower():
            benefic_dignity = p.get("dignity", "peregrine").lower()
            break

    strong = benefic_dignity in ("exaltation", "domicile")

    if benefic == "Jupiter" and strong:
        statement = ("Jupiter is your luck star. Strong placement in your chart. You're designed to attract opportunities. "
                     "TRUE: Good things that come to me tend to stick. Wins compound over time. "
                     "FALSE: Opportunities show up but slip away or never quite land.")
    elif benefic == "Jupiter" and not strong:
        statement = ("Jupiter is your luck star, but it's in a weak placement. Opportunities have to be worked for. "
                     "TRUE: My breaks have been real, even if I had to earn every one of them. "
                     "FALSE: I feel like I've been promised a lot of opportunities that never came through.")
    elif benefic == "Venus" and strong:
        statement = ("Venus is your luck star. Strong placement. You're designed to be lucky in relationships, beauty, and pleasure. "
                     "TRUE: Good things that come to me tend to stick. My life has real warmth and connection in it. "
                     "FALSE: Opportunities for love and good fortune show up but often slip away.")
    else:
        statement = ("Venus is your luck star, but it's in a weak placement. Good things have to be held tight or they fade. "
                     "TRUE: My good things have been real, even if I had to fight to keep them. "
                     "FALSE: I've had chances at love and beauty that I couldn't hold onto.")

    return {
        "id": "q4_benefic_expression",
        "tier": 2,
        "fork": "benefic_landing",
        "statement": statement,
        "impact": f"If TRUE: {benefic}'s gifts are landing - predict compounding blessings. If FALSE: blessings slip - predict almost-wins, deferred opportunities.",
    }


def q5_malefic_expression(hellenistic: dict) -> dict:
    sect = hellenistic.get("sect", "night")
    malefic = "Mars" if sect == "day" else "Saturn"

    if malefic == "Saturn":
        statement = ("Saturn is your testing star. It forces discipline, delay, and restriction into your life. "
                     "TRUE: I have strong discipline. I finish what I start, even when it's hard. "
                     "FALSE: I delay, procrastinate, or avoid difficult things - and I pay for it later.")
    else:
        statement = ("Mars is your testing star. It forces confrontation, anger, and competition into your life. "
                     "TRUE: I channel my anger productively. I fight for what matters. "
                     "FALSE: My anger comes out sideways - passive-aggression, burnout, explosive moments I regret.")

    return {
        "id": "q5_malefic_expression",
        "tier": 2,
        "fork": "malefic_channel",
        "statement": statement,
        "impact": f"If TRUE: {malefic} operates as productive discipline. If FALSE: {malefic} operates as obstacle - predict repeated frustration in its domain.",
    }


def q6_profection_quality(hellenistic: dict) -> dict:
    planets = hellenistic.get("planets", [])

    dignified_count = 0
    weak_count = 0
    for p in planets:
        dig = p.get("dignity", "peregrine").lower()
        if dig in ("exaltation", "domicile"):
            dignified_count += 1
        elif dig in ("fall", "detriment"):
            weak_count += 1

    if dignified_count > weak_count:
        statement = ("On paper, you should be lucky. Your chart has more strong planets than weak ones. "
                     "TRUE: My life has mostly worked out. I've had real breaks and advantages. "
                     "FALSE: My life looks lucky from the outside, but it's been harder inside than anyone knows.")
        impact = "If TRUE: predict clean delivery, opportunities landing on time. If FALSE: predict internal struggles despite external success."
    elif weak_count > dignified_count:
        statement = ("Your chart shows more obstacles than easy paths. You've had to build from disadvantage. "
                     "TRUE: Yes - things haven't come easy. I've built what I have against real resistance. "
                     "FALSE: Things have worked out more than the chart suggests. Effort wasn't the main issue.")
        impact = "If TRUE: predict hard-won wins, years of preparation before payoff. If FALSE: lean toward easier readings."
    else:
        statement = ("Your chart has a balance of strong and weak placements. Both fortune and frustration are written in. "
                     "TRUE: My life has clear cycles of wins and losses in roughly equal measure. "
                     "FALSE: One mode dominates - I'm either mostly lucky or mostly struggling, not both.")
        impact = "If TRUE: alternating good/hard years. If FALSE: predict one dominant mode across all years."

    return {
        "id": "q6_profection_quality",
        "tier": 2,
        "fork": "lord_delivery",
        "statement": statement,
        "impact": impact,
    }


# ═══════════════════════════════════════════════════════════
# TIER 3: ZWDS STARS (Manifestation)
# ═══════════════════════════════════════════════════════════

def q7_leader_vs_supporter(zwds: dict) -> dict:
    palaces = zwds.get("palaces", [])
    life_stars = find_palace_stars(palaces, "Life")
    life_has_ziwei_group = any(s in ZIWEI_GROUP for s in life_stars)
    life_has_tianfu_group = any(s in TIANFU_GROUP for s in life_stars)

    if life_has_ziwei_group and not life_has_tianfu_group:
        statement = ("Your chart is built for leadership. You're designed to be out front, not behind. "
                     "TRUE: I'd rather lead and carry full responsibility than work for someone else. "
                     "FALSE: I do my best work as the trusted second - being out front actually drains me.")
    elif life_has_tianfu_group and not life_has_ziwei_group:
        statement = ("Your chart is built for stewardship. You're designed to be the trusted builder, not the one on the stage. "
                     "TRUE: I do my best work supporting a strong leader or mission. I don't need the spotlight. "
                     "FALSE: I belong at the front. Supporting others has never felt right to me.")
    else:
        statement = ("Your chart shows you can go either way - lead or support - depending on the situation. "
                     "TRUE: I'd rather lead and carry full responsibility. "
                     "FALSE: I'd rather support a strong leader than be the one out front.")

    return {
        "id": "q7_leader_vs_supporter",
        "tier": 3,
        "fork": "authority_orientation",
        "statement": statement,
        "impact": "If TRUE: activate leadership readings - authority, visibility, solo responsibility. If FALSE: activate stewardship readings - trusted support, accumulation.",
    }


def q8_destruction_expression(zwds: dict) -> dict:
    palaces = zwds.get("palaces", [])
    qisha_palace = find_star_palace(palaces, "qi_sha")
    pojun_palace = find_star_palace(palaces, "po_jun")

    if qisha_palace and pojun_palace:
        statement = ("Your chart points to major rupture - something that breaks and then rebuilds. You've either lived through it or it's still ahead. "
                     "TRUE: I've already been through something that broke me apart. I'm rebuilding from it. "
                     "FALSE: Life has been mostly stable. The rupture hasn't hit yet.")
    elif qisha_palace:
        statement = ("Your chart points to a major crisis around destiny or life direction - rupture that forces you to redefine what you're doing. "
                     "TRUE: I've already been through the reset. I know what it feels like. "
                     "FALSE: That hasn't happened yet. My sense of direction has been steady.")
    elif pojun_palace:
        statement = ("Your chart points to major relocation, migration, or uprooting - a complete break from where you started. "
                     "TRUE: I've already lived through a major relocation or life reset. I'm not in my original place anymore. "
                     "FALSE: I've stayed close to my roots. No dramatic uprooting yet.")
    else:
        statement = ("Your chart doesn't show catastrophic rupture, but life still tests you in quieter ways. "
                     "TRUE: I've been through a period that would have broken most people. I came out of it. "
                     "FALSE: My life has been more steady than dramatic. No make-or-break period yet.")

    return {
        "id": "q8_destruction_expression",
        "tier": 3,
        "fork": "destruction_timing",
        "statement": statement,
        "impact": "If TRUE: rupture has already manifested - predict rebuilding arc, resurrection themes. If FALSE: predict rupture as still ahead.",
    }


def q9_appetite_vs_discipline(zwds: dict) -> dict:
    palaces = zwds.get("palaces", [])
    tanlang_palace = find_star_palace(palaces, "tan_lang")
    wuqu_palace = find_star_palace(palaces, "wu_qu")

    tanlang_in_spouse = tanlang_palace == "Spouse"
    wuqu_in_career = wuqu_palace == "Career"

    if tanlang_in_spouse and wuqu_in_career:
        statement = ("Your chart points to hunger in relationships and discipline in work. Which have you actually lived? "
                     "TRUE: I've followed my appetites in love - many relationships, experiences, or indulgences. "
                     "FALSE: I've stayed disciplined and focused in work - fewer relationships, a narrower path.")
    elif tanlang_palace:
        statement = ("Your chart points to strong appetite and charisma in your life - many options, many experiences possible. "
                     "TRUE: I've followed that. Multiple meaningful relationships, lots of experience. "
                     "FALSE: I've restrained it. I chose depth over variety.")
    elif wuqu_palace:
        statement = ("Your chart points to strong discipline and measured effort in your life - structured, consistent, focused. "
                     "TRUE: I've applied that. My path has been deliberate and narrow. "
                     "FALSE: I've been looser than my chart suggests. Discipline is still developing.")
    else:
        statement = ("Your chart doesn't lean hard toward appetite or discipline. You get to choose which mode defines you. "
                     "TRUE: My life has been about appetite - many experiences, relationships, and pursuits. "
                     "FALSE: My life has been about discipline - fewer things, deeper commitment.")

    return {
        "id": "q9_appetite_vs_discipline",
        "tier": 3,
        "fork": "appetite_vs_discipline",
        "statement": statement,
        "impact": "If TRUE (appetite): predict multi-stream activity, many threads, charisma-based wins. If FALSE (discipline): predict fewer but deeper arcs, structured achievement.",
    }


# ═══════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════

def generate_clarifying_questions(nayin_data: dict, hellenistic: dict, zwds: dict) -> list:
    return [
        q1_nayin_visibility(nayin_data),
        q2_nayin_strength(nayin_data),
        q3_sect_condition(hellenistic),
        q4_benefic_expression(hellenistic),
        q5_malefic_expression(hellenistic),
        q6_profection_quality(hellenistic),
        q7_leader_vs_supporter(zwds),
        q8_destruction_expression(zwds),
        q9_appetite_vs_discipline(zwds),
    ]


def format_answers_for_llm(questions: list, answers: dict) -> str:
    if not answers:
        return ""

    lines = ["═══ USER STANCE (from 9 clarifying questions) ═══",
             "These are the user's explicit answers. USE THEM to tilt interpretation.",
             "When an answer contradicts what the chart suggests alone, TRUST THE ANSWER - they know their life.",
             ""]

    for q in questions:
        qid = q["id"]
        if qid not in answers:
            continue
        ans = answers[qid]
        ans_str = "TRUE" if ans else "FALSE"
        lines.append(f"[{qid}] Answer: {ans_str}")
        lines.append(f"  Fork: {q['fork']}")
        lines.append(f"  Direction: {q['impact']}")
        lines.append("")

    return "\n".join(lines)
