"""
Starlogic — Clarifying Questions Generator
Inspects a chart and generates 9 tailored True/False questions across 3 tiers:
  Tier 1 (Nayin + Sect): how the operating system runs
  Tier 2 (Hellenistic): how planets deliver
  Tier 3 (ZWDS stars): how stars manifest

Each answered question tilts the LLM's interpretation toward the chosen path.
"""

# ═══════════════════════════════════════════════════════════
# NAYIN CATEGORIZATION (for Tier 1 question selection)
# ═══════════════════════════════════════════════════════════

NAYIN_VISIBILITY_HIDDEN = {
    "hai_zhong_jin", "sha_zhong_jin", "jian_xia_shui", "lu_zhong_huo",
    "shan_xia_huo", "fu_deng_huo",
}
NAYIN_VISIBILITY_EXPOSED = {
    "jian_feng_jin", "shan_tou_huo", "pi_li_huo", "tian_shang_huo",
    "da_lin_mu", "chang_liu_shui", "da_xi_shui", "tian_he_shui",
    "da_hai_shui", "wu_shang_tu", "tian_shang_huo",
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
DESTRUCTIVE_STARS = {"qi_sha", "po_jun"}
APPETITE_STARS = {"tan_lang"}
DISCIPLINE_STARS = {"wu_qu"}

STAR_CHINESE_NAMES = {
    "zi_wei": "Zi Wei (Purple Emperor)", "tian_ji": "Tian Ji (Heavenly Mechanism)",
    "tai_yang": "Tai Yang (Sun)", "wu_qu": "Wu Qu (Military Wealth)",
    "tian_tong": "Tian Tong (Heavenly Unity)", "lian_zhen": "Lian Zhen (Chastity)",
    "tian_fu": "Tian Fu (Celestial Vault)", "tai_yin": "Tai Yin (Moon)",
    "tan_lang": "Tan Lang (Greedy Wolf)", "ju_men": "Ju Men (Giant Gate)",
    "tian_xiang": "Tian Xiang (Heavenly Minister)",
    "tian_liang": "Tian Liang (Celestial Beam)",
    "qi_sha": "Qi Sha (Seven Killings)", "po_jun": "Po Jun (Army Breaker)",
}

PALACE_ENGLISH_TO_DOMAIN = {
    "Life": "self-identity", "Siblings": "peer dynamics",
    "Spouse": "partnership", "Children": "creative output",
    "Wealth": "financial life", "Health": "body and vitality",
    "Travel": "movement and change", "Friends": "social network",
    "Career": "professional path", "Property": "home and foundation",
    "Fortune": "fate and luck", "Parents": "authority figures",
}


# ═══════════════════════════════════════════════════════════
# HELPER: FIND STAR LOCATIONS IN PALACES
# ═══════════════════════════════════════════════════════════

def find_star_palace(zwds_palaces: list, target_star: str) -> str:
    """Return English palace name where target_star sits, or empty string."""
    for p in zwds_palaces:
        stars = p.get("stars", [])
        if isinstance(stars, list):
            for s in stars:
                pinyin = s.get("pinyin", "") if isinstance(s, dict) else str(s)
                if pinyin == target_star:
                    return p.get("name_english", "")
    return ""


def find_palace_stars(zwds_palaces: list, target_palace: str) -> list:
    """Return pinyin list of stars in a given palace."""
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
    """Hidden builder vs public presence — how the person's work becomes known."""
    pinyin = nayin_data.get("pinyin", "")
    english = nayin_data.get("english_name", "your nayin")

    if pinyin in NAYIN_VISIBILITY_HIDDEN:
        statement = (f"Your nayin is {english}, which builds out of sight. "
                     "TRUE: I'm comfortable building quietly for years before recognition arrives. "
                     "FALSE: I want visible progress now and struggle with slow invisible work.")
    elif pinyin in NAYIN_VISIBILITY_EXPOSED:
        statement = (f"Your nayin is {english}, which operates in the open. "
                     "TRUE: I do my best work when others can see it — I need the stage. "
                     "FALSE: I prefer working behind the scenes and get drained by being visible.")
    else:
        statement = (f"Your nayin is {english}. "
                     "TRUE: I prefer working on things where progress is visible to others. "
                     "FALSE: I prefer working on things where the payoff comes after years of quiet effort.")

    return {
        "id": "q1_nayin_visibility",
        "tier": 1,
        "fork": "visibility",
        "statement": statement,
        "impact": "If TRUE: interpret toward public-facing outcomes (recognition, visible milestones). If FALSE: interpret toward long compound arcs, late-blooming wins.",
    }


def q2_nayin_strength(nayin_data: dict) -> dict:
    """Endurance vs adaptability."""
    pinyin = nayin_data.get("pinyin", "")
    english = nayin_data.get("english_name", "your nayin")

    if pinyin in NAYIN_STRENGTH_ENDURING:
        statement = (f"Your nayin ({english}) has enduring strength. "
                     "TRUE: When something breaks me, I take years to fully recover but emerge stronger. "
                     "FALSE: I bounce back quickly from setbacks and don't dwell on them.")
    elif pinyin in NAYIN_STRENGTH_ADAPTIVE:
        statement = (f"Your nayin ({english}) has adaptive strength. "
                     "TRUE: I change direction when needed without attachment to the old plan. "
                     "FALSE: Once I commit to a path, I stick with it even when it stops working.")
    else:
        statement = ("TRUE: When life pressures me, I adapt and reshape myself fluidly. "
                     "FALSE: When life pressures me, I hold my ground and wait it out.")

    return {
        "id": "q2_nayin_strength",
        "tier": 1,
        "fork": "strength",
        "statement": statement,
        "impact": "If TRUE (adaptive): predict pivots, resets, new beginnings after setbacks. If FALSE (enduring): predict long single arcs with deep recovery periods.",
    }


def q3_sect_condition(hellenistic: dict) -> dict:
    """Sect light active vs dormant."""
    sect = hellenistic.get("sect", "unknown")
    sect_light = "Sun" if sect == "day" else "Moon" if sect == "night" else "your sect light"

    planets = hellenistic.get("planets", [])
    light_dignity = "peregrine"
    for p in planets:
        if p.get("name", "").lower() == sect_light.lower():
            light_dignity = p.get("dignity", "peregrine").lower()
            break

    if sect == "day":
        statement = ("You were born during the day — the Sun is your sect light. "
                     "TRUE: I feel most alive taking charge, being seen, and moving outward. "
                     "FALSE: I feel drained by constant visibility and recharge in privacy.")
    elif sect == "night":
        statement = ("You were born at night — the Moon is your sect light. "
                     "TRUE: I feel most alive in reflective, emotionally connected spaces. "
                     "FALSE: I prefer action and external achievement over inner emotional work.")
    else:
        statement = ("TRUE: I run on intuition and emotional reading of situations. "
                     "FALSE: I run on logic and external achievement.")

    return {
        "id": "q3_sect_condition",
        "tier": 1,
        "fork": "sect_alignment",
        "statement": statement,
        "impact": f"If TRUE: sect light ({sect_light}, {light_dignity}) is actively running — predict its domain strongly. If FALSE: sect light dormant, its natal house themes underactive.",
    }


# ═══════════════════════════════════════════════════════════
# TIER 2: HELLENISTIC (Planetary Delivery)
# ═══════════════════════════════════════════════════════════

def q4_benefic_expression(hellenistic: dict) -> dict:
    """Are blessings landing or slipping?"""
    sect = hellenistic.get("sect", "night")
    benefic_of_sect = "Jupiter" if sect == "day" else "Venus"

    planets = hellenistic.get("planets", [])
    benefic_dignity = "peregrine"
    benefic_house = 1
    for p in planets:
        if p.get("name", "").lower() == benefic_of_sect.lower():
            benefic_dignity = p.get("dignity", "peregrine").lower()
            benefic_house = p.get("house", 1)
            break

    statement = (f"{benefic_of_sect} is your sect benefic (the star that should bring blessings), "
                 f"currently at {benefic_dignity} dignity in the {benefic_house}th house. "
                 "TRUE: Good things that come to me tend to stick and compound over time. "
                 "FALSE: Opportunities arrive but frequently slip through my hands or fail to materialize.")

    return {
        "id": "q4_benefic_expression",
        "tier": 2,
        "fork": "benefic_landing",
        "statement": statement,
        "impact": f"If TRUE: {benefic_of_sect}'s gifts are landing — predict compounding blessings, stable gains. If FALSE: blessings slip — predict almost-wins, deferred opportunities, recovery arcs.",
    }


def q5_malefic_expression(hellenistic: dict) -> dict:
    """Malefic as discipline vs obstacle?"""
    sect = hellenistic.get("sect", "night")
    malefic_out_of_sect = "Mars" if sect == "day" else "Saturn"

    planets = hellenistic.get("planets", [])
    malefic_dignity = "peregrine"
    malefic_house = 1
    for p in planets:
        if p.get("name", "").lower() == malefic_out_of_sect.lower():
            malefic_dignity = p.get("dignity", "peregrine").lower()
            malefic_house = p.get("house", 1)
            break

    if malefic_out_of_sect == "Saturn":
        statement = (f"Saturn is your out-of-sect malefic (the star that tests you) at {malefic_dignity} dignity in house {malefic_house}. "
                     "TRUE: I have strong self-discipline and complete what I start even when it's hard. "
                     "FALSE: I procrastinate, delay, or avoid difficult things and often regret it later.")
    else:
        statement = (f"Mars is your out-of-sect malefic at {malefic_dignity} dignity in house {malefic_house}. "
                     "TRUE: I channel anger and confrontation productively — I fight for what matters. "
                     "FALSE: My anger comes out sideways — passive-aggression, burnout, or explosive episodes.")

    return {
        "id": "q5_malefic_expression",
        "tier": 2,
        "fork": "malefic_channel",
        "statement": statement,
        "impact": f"If TRUE: {malefic_out_of_sect} operates as productive discipline — predict achievement through pressure. If FALSE: {malefic_out_of_sect} operates as obstacle — predict repeated frustration in its house domain.",
    }


def q6_profection_quality(hellenistic: dict) -> dict:
    """Does the profection lord deliver cleanly or frustrated?"""
    planets = hellenistic.get("planets", [])

    # Count dignified vs weak planets
    dignified_count = 0
    weak_count = 0
    for p in planets:
        dig = p.get("dignity", "peregrine").lower()
        if dig in ("exaltation", "domicile"):
            dignified_count += 1
        elif dig in ("fall", "detriment"):
            weak_count += 1

    if weak_count > dignified_count:
        statement = ("Your chart has more planets in weak condition than strong. "
                     "TRUE: My life has required me to build from disadvantage — things don't come easy. "
                     "FALSE: Things have generally worked out when I put in moderate effort.")
        impact = "If TRUE: predict hard-won wins, years of preparation before payoff. If FALSE: assume dignity is overstating disadvantage — lean toward easier readings."
    elif dignified_count > weak_count:
        statement = ("Your chart has more planets in strong condition than weak. "
                     "TRUE: Things have mostly gone well for me — I've had real breaks and advantages. "
                     "FALSE: Despite external indicators of luck, my inner experience has been harder than it looks.")
        impact = "If TRUE: predict clean delivery, opportunities landing on time. If FALSE: predict internal struggles despite external success — hidden friction."
    else:
        statement = ("Your chart has mixed planetary conditions. "
                     "TRUE: My life has clear themes of both fortune and frustration — wins and losses in balance. "
                     "FALSE: One mode dominates my life — I'm either generally lucky or generally struggling, not both.")
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
    """Zi Wei group (leader) vs Tian Fu group (builder/supporter) orientation."""
    palaces = zwds.get("palaces", [])

    # Find where Zi Wei and Tian Fu sit
    ziwei_palace = find_star_palace(palaces, "zi_wei")
    tianfu_palace = find_star_palace(palaces, "tian_fu")

    # Check Life palace stars
    life_stars = find_palace_stars(palaces, "Life")
    life_has_ziwei_group = any(s in ZIWEI_GROUP for s in life_stars)
    life_has_tianfu_group = any(s in TIANFU_GROUP for s in life_stars)

    if life_has_ziwei_group and not life_has_tianfu_group:
        statement = (f"Your Life palace carries the Zi Wei group (authority, command). "
                     f"Zi Wei sits in {ziwei_palace}, Tian Fu in {tianfu_palace}. "
                     "TRUE: I'd rather lead and take the blame than support and share credit. "
                     "FALSE: I'm most valuable as the #2 — I make leaders effective without wanting their job.")
    elif life_has_tianfu_group and not life_has_ziwei_group:
        statement = (f"Your Life palace carries the Tian Fu group (accumulation, support). "
                     f"Tian Fu sits in {tianfu_palace}, Zi Wei in {ziwei_palace}. "
                     "TRUE: I'm most valuable as the trusted builder/second — not center stage. "
                     "FALSE: I belong at the front — supporting others never felt right to me.")
    else:
        statement = (f"Zi Wei sits in your {ziwei_palace} palace; Tian Fu in your {tianfu_palace} palace. "
                     "TRUE: I'd rather lead and take full responsibility than be second-in-command. "
                     "FALSE: I thrive behind a strong leader rather than being the one out front.")

    return {
        "id": "q7_leader_vs_supporter",
        "tier": 3,
        "fork": "authority_orientation",
        "statement": statement,
        "impact": f"If TRUE: activate Zi Wei ({ziwei_palace}) readings around authority, visibility, solo responsibility. If FALSE: activate Tian Fu ({tianfu_palace}) readings around stewardship, trusted support, accumulation.",
    }


def q8_destruction_expression(zwds: dict) -> dict:
    """Qi Sha / Po Jun — already manifested or still pending?"""
    palaces = zwds.get("palaces", [])

    qisha_palace = find_star_palace(palaces, "qi_sha")
    pojun_palace = find_star_palace(palaces, "po_jun")

    if qisha_palace and pojun_palace:
        domain_qs = PALACE_ENGLISH_TO_DOMAIN.get(qisha_palace, qisha_palace.lower())
        domain_pj = PALACE_ENGLISH_TO_DOMAIN.get(pojun_palace, pojun_palace.lower())
        statement = (f"Qi Sha (destruction) sits in your {qisha_palace} palace ({domain_qs}), "
                     f"and Po Jun (demolition) in your {pojun_palace} ({domain_pj}). "
                     f"TRUE: A major crisis has already hit my {domain_qs} or {domain_pj} — I've lived through and rebuilt from it. "
                     f"FALSE: These areas of my life have been stable — no major rupture yet.")
    elif qisha_palace:
        domain = PALACE_ENGLISH_TO_DOMAIN.get(qisha_palace, qisha_palace.lower())
        statement = (f"Qi Sha (destruction) sits in your {qisha_palace} palace — the area of {domain}. "
                     f"TRUE: I've already been through a major crisis or loss in {domain} and rebuilt. "
                     f"FALSE: This area of my life hasn't seen its reckoning yet.")
    elif pojun_palace:
        domain = PALACE_ENGLISH_TO_DOMAIN.get(pojun_palace, pojun_palace.lower())
        statement = (f"Po Jun (demolition) sits in your {pojun_palace} palace — the area of {domain}. "
                     f"TRUE: I've already demolished and rebuilt my {domain} from the ground up. "
                     f"FALSE: This area hasn't been through its breakdown yet.")
    else:
        statement = ("TRUE: I've survived a period that would have broken most people — it's behind me. "
                     "FALSE: The biggest rupture of my life is still ahead of me.")

    return {
        "id": "q8_destruction_expression",
        "tier": 3,
        "fork": "destruction_timing",
        "statement": statement,
        "impact": "If TRUE: the Qi Sha/Po Jun energy has already manifested — predict the rebuilding arc, resurrection themes. If FALSE: predict the rupture event as still ahead, flag the years where it's most likely.",
    }


def q9_appetite_vs_discipline(zwds: dict) -> dict:
    """Tan Lang appetite vs Wu Qu discipline."""
    palaces = zwds.get("palaces", [])

    tanlang_palace = find_star_palace(palaces, "tan_lang")
    wuqu_palace = find_star_palace(palaces, "wu_qu")

    if tanlang_palace and wuqu_palace:
        tl_domain = PALACE_ENGLISH_TO_DOMAIN.get(tanlang_palace, tanlang_palace.lower())
        wq_domain = PALACE_ENGLISH_TO_DOMAIN.get(wuqu_palace, wuqu_palace.lower())
        statement = (f"Tan Lang (appetite, charisma) sits in your {tanlang_palace} ({tl_domain}); "
                     f"Wu Qu (discipline, calculated effort) sits in your {wuqu_palace} ({wq_domain}). "
                     f"TRUE: I've followed my appetites in {tl_domain} — many relationships, experiences, or indulgences. "
                     f"FALSE: I've applied discipline in {wq_domain} and restrained appetite — I chose structure over variety.")
    elif tanlang_palace:
        domain = PALACE_ENGLISH_TO_DOMAIN.get(tanlang_palace, tanlang_palace.lower())
        statement = (f"Tan Lang (appetite) sits in your {tanlang_palace} — area of {domain}. "
                     f"TRUE: I've followed appetite in {domain} — many options, experiences, or relationships. "
                     f"FALSE: I've restrained this appetite and chose a narrower, more disciplined path.")
    elif wuqu_palace:
        domain = PALACE_ENGLISH_TO_DOMAIN.get(wuqu_palace, wuqu_palace.lower())
        statement = (f"Wu Qu (discipline) sits in your {wuqu_palace} — area of {domain}. "
                     f"TRUE: I've applied serious discipline to {domain} — structured, measured, consistent. "
                     f"FALSE: I've been looser here than my chart suggests — discipline is still developing.")
    else:
        statement = ("TRUE: My life story is one of appetite — many experiences, relationships, or pursuits. "
                     "FALSE: My life story is one of discipline — narrow focus, fewer but deeper commitments.")

    return {
        "id": "q9_appetite_vs_discipline",
        "tier": 3,
        "fork": "appetite_vs_discipline",
        "statement": statement,
        "impact": "If TRUE (appetite): predict multi-stream activity, many threads, charisma-based wins. If FALSE (discipline): predict fewer but deeper arcs, structured compound achievement.",
    }


# ═══════════════════════════════════════════════════════════
# MAIN GENERATOR
# ═══════════════════════════════════════════════════════════

def generate_clarifying_questions(nayin_data: dict, hellenistic: dict, zwds: dict) -> list:
    """Generate all 9 tailored clarifying questions for this chart."""
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
    """Format the user's answers as an LLM-consumable stance block.
    answers is a dict: {"q1_nayin_visibility": True, "q2_nayin_strength": False, ...}"""
    if not answers:
        return ""

    lines = ["═══ USER STANCE (from 9 clarifying questions) ═══",
             "These are the user's explicit answers. USE THEM to tilt interpretation.",
             "When an answer contradicts what the chart suggests alone, TRUST THE ANSWER — they know their life.",
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
