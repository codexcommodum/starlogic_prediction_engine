"""
Starlogic Prediction Engine — Orchestrator Service
Calls Hellenistic + ZWDS engines, runs 7-layer computation, scores convergence.
Returns pre-scored signals. LLM narrative handled by frontend (Base44 InvokeLLM).
"""

import os
import math
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Age-specific star-palace interpretations
from star_palace_age_effects import get_star_palace_age_effect, get_age_bracket
from clarifying_questions import generate_clarifying_questions, format_answers_for_llm
from theme_bridge import build_year_themes, is_compression_year

app = FastAPI(title="Starlogic Prediction Engine", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ═══════════════════════════════════════════════════════════
# SERVICE URLs
# ═══════════════════════════════════════════════════════════
HELLENISTIC_URL = os.getenv("HELLENISTIC_URL", "https://starlogichellenisticengine-production.up.railway.app")
ZWDS_URL = os.getenv("ZWDS_URL", "https://starlogiczwdsengine-production.up.railway.app")

# ═══════════════════════════════════════════════════════════
# CACHE (in-memory for now, swap to Redis later)
# ═══════════════════════════════════════════════════════════
READING_CACHE = {}

# ═══════════════════════════════════════════════════════════
# REFERENCE DATA
# ═══════════════════════════════════════════════════════════

TRADITIONAL_RULERS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

SIGN_ORDER = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
              "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

HOUSE_THEMES = {
    1: {"keywords":["self","body","identity","personal_initiative","appearance"],"short":"self and body"},
    2: {"keywords":["money","possessions","resources","earning","values"],"short":"money and resources"},
    3: {"keywords":["communication","siblings","local_environment","learning","short_travel"],"short":"communication and learning"},
    4: {"keywords":["home","family","father","roots","real_estate","foundation"],"short":"home and roots"},
    5: {"keywords":["children","creativity","pleasure","romance","joy","speculation"],"short":"children and creativity"},
    6: {"keywords":["health","work","daily_routine","service","illness"],"short":"health and daily work"},
    7: {"keywords":["partnerships","marriage","open_enemies","the_other","contracts"],"short":"partnerships and rivals"},
    8: {"keywords":["shared_resources","transformation","death_rebirth","inheritance","insurance","hidden_wealth","intimacy"],"short":"transformation and shared resources"},
    9: {"keywords":["higher_education","travel","philosophy","legal","publishing","foreign"],"short":"education and philosophy"},
    10:{"keywords":["career","public_reputation","authority","achievement","status"],"short":"career and public life"},
    11:{"keywords":["friends","allies","community","hopes","networks","groups"],"short":"friends and community"},
    12:{"keywords":["isolation","hidden_enemies","self_undoing","endings","unconscious","secrets","withdrawal"],"short":"isolation and hidden matters"},
}

PALACE_THEMES = {
    "Life":{"keywords":["self","identity","body","destiny","personality"],"short":"self-formation and personal destiny"},
    "Siblings":{"keywords":["peers","rivalry","social_identity","belonging","competition"],"short":"peer dynamics and social positioning"},
    "Spouse":{"keywords":["partnerships","marriage","business_alliances","the_other"],"short":"partnerships and the defining Other"},
    "Children":{"keywords":["creative_output","offspring","legacy","production","joy"],"short":"creative legacy and offspring"},
    "Wealth":{"keywords":["assets","accumulation","financial_sovereignty","security"],"short":"financial sovereignty and asset building"},
    "Health":{"keywords":["vitality","emotional_stability","illness","body_signals"],"short":"physical and emotional health"},
    "Travel":{"keywords":["movement","change","exploration","restlessness","relocation"],"short":"movement and external exploration"},
    "Friends":{"keywords":["social_network","benefactors","professional_connections"],"short":"social network and benefactors"},
    "Career":{"keywords":["profession","public_role","ambition","authority","achievement"],"short":"professional path and public role"},
    "Property":{"keywords":["real_estate","home_base","ancestral_wealth","physical_foundation"],"short":"real estate and physical foundation"},
    "Fortune":{"keywords":["luck","fate","blessings","karmic_inheritance","destiny_pivot"],"short":"luck and fate"},
    "Parents":{"keywords":["parental_influence","authority_figures","inherited_patterns"],"short":"parental influence and inherited patterns"},
}

DIGNITY_SCORES = {
    "exaltation": {"score":1.0,"quality":"excellent","effect":"delivers_more_than_expected"},
    "domicile":   {"score":0.9,"quality":"strong","effect":"functions_naturally_and_powerfully"},
    "peregrine":  {"score":0.15,"quality":"unanchored","effect":"wandering_unfocused"},
    "fall":       {"score":0.1,"quality":"weak","effect":"promises_that_disappoint"},
    "detriment":  {"score":0.05,"quality":"hostile","effect":"works_against_its_nature"},
}

NAYIN_PROPERTIES = {
    "hai_zhong_jin":{"visibility":"hidden","strength":"enduring","recognition":"delayed_then_sudden"},
    "jian_feng_jin":{"visibility":"exposed","strength":"sharp","recognition":"immediate_threat"},
    "bai_la_jin":{"visibility":"subtle","strength":"flexible","recognition":"crafted"},
    "sha_zhong_jin":{"visibility":"buried","strength":"latent","recognition":"requires_effort"},
    "jin_bo_jin":{"visibility":"surface","strength":"fragile","recognition":"decorative"},
    "cha_chuan_jin":{"visibility":"worn","strength":"refined","recognition":"earned"},
    "lu_zhong_huo":{"visibility":"contained","strength":"controlled","recognition":"industrial"},
    "shan_tou_huo":{"visibility":"prominent","strength":"wild","recognition":"visible_danger"},
    "shan_xia_huo":{"visibility":"low","strength":"smoldering","recognition":"delayed_ignition"},
    "pi_li_huo":{"visibility":"explosive","strength":"sudden","recognition":"unavoidable"},
    "fu_deng_huo":{"visibility":"dim","strength":"fragile","recognition":"needs_protection"},
    "tian_shang_huo":{"visibility":"supreme","strength":"overwhelming","recognition":"divine"},
    "da_lin_mu":{"visibility":"massive","strength":"rooted","recognition":"undeniable"},
    "yang_liu_mu":{"visibility":"graceful","strength":"flexible","recognition":"beauty"},
    "song_bai_mu":{"visibility":"evergreen","strength":"enduring","recognition":"respected"},
    "ping_di_mu":{"visibility":"flat","strength":"widespread","recognition":"common"},
    "shi_liu_mu":{"visibility":"fruiting","strength":"productive","recognition":"harvest"},
    "sang_zhe_mu":{"visibility":"useful","strength":"practical","recognition":"functional"},
    "jian_xia_shui":{"visibility":"hidden","strength":"flowing","recognition":"discovered"},
    "quan_zhong_shui":{"visibility":"emerging","strength":"fresh","recognition":"source"},
    "chang_liu_shui":{"visibility":"exposed","strength":"persistent","recognition":"constant"},
    "da_xi_shui":{"visibility":"powerful","strength":"rushing","recognition":"forceful"},
    "tian_he_shui":{"visibility":"celestial","strength":"vast","recognition":"cosmic"},
    "da_hai_shui":{"visibility":"immense","strength":"unfathomable","recognition":"overwhelming"},
    "lu_pang_tu":{"visibility":"exposed","strength":"trampled","recognition":"overlooked"},
    "cheng_tou_tu":{"visibility":"elevated","strength":"defensive","recognition":"structural"},
    "wu_shang_tu":{"visibility":"high","strength":"exposed","recognition":"prominent"},
    "bi_shang_tu":{"visibility":"vertical","strength":"applied","recognition":"functional"},
    "da_yi_tu":{"visibility":"vast","strength":"load_bearing","recognition":"foundational"},
    "sha_zhong_tu":{"visibility":"mixed","strength":"unstable","recognition":"uncertain"},
}

ELEMENT_INTERACTIONS = {
    ("WOOD","FIRE"):"PRODUCES",("FIRE","EARTH"):"PRODUCES",("EARTH","METAL"):"PRODUCES",
    ("METAL","WATER"):"PRODUCES",("WATER","WOOD"):"PRODUCES",
    ("WOOD","EARTH"):"CONTROLS",("EARTH","WATER"):"CONTROLS",("WATER","FIRE"):"CONTROLS",
    ("FIRE","METAL"):"CONTROLS",("METAL","WOOD"):"CONTROLS",
    ("WOOD","WOOD"):"SAME",("FIRE","FIRE"):"SAME",("EARTH","EARTH"):"SAME",
    ("METAL","METAL"):"SAME",("WATER","WATER"):"SAME",
}

INTERACTION_SCORES = {
    "PRODUCES":1.0,"CONTROLS":-0.8,"SAME":0.8,"PRODUCED_BY":-0.5,"CONTROLLED_BY":0.6,"NEUTRAL":0.0,
}

STEMS = [
    {"name":"Jia","polarity":"Yang","element":"WOOD"},{"name":"Yi","polarity":"Yin","element":"WOOD"},
    {"name":"Bing","polarity":"Yang","element":"FIRE"},{"name":"Ding","polarity":"Yin","element":"FIRE"},
    {"name":"Wu","polarity":"Yang","element":"EARTH"},{"name":"Ji","polarity":"Yin","element":"EARTH"},
    {"name":"Geng","polarity":"Yang","element":"METAL"},{"name":"Xin","polarity":"Yin","element":"METAL"},
    {"name":"Ren","polarity":"Yang","element":"WATER"},{"name":"Gui","polarity":"Yin","element":"WATER"},
]
BRANCHES = [
    {"name":"Zi","element":"WATER"},{"name":"Chou","element":"EARTH"},
    {"name":"Yin","element":"WOOD"},{"name":"Mao","element":"WOOD"},
    {"name":"Chen","element":"EARTH"},{"name":"Si","element":"FIRE"},
    {"name":"Wu","element":"FIRE"},{"name":"Wei","element":"EARTH"},
    {"name":"Shen","element":"METAL"},{"name":"You","element":"METAL"},
    {"name":"Xu","element":"EARTH"},{"name":"Hai","element":"WATER"},
]

# Star-palace effects database (14 stars × 12 palaces)
STAR_PALACE_EFFECTS = {
    "zi_wei":{"Life":"born leader strong personal destiny","Siblings":"dominance among peers","Spouse":"dominant partner marriage to powerful person","Children":"children of significance","Wealth":"imperial finances sovereign control","Health":"strong constitution pride blocks treatment","Travel":"purposeful dignified journeys","Friends":"powerful allies few true equals","Career":"high authority executive power","Property":"estate ownership commanding residence","Fortune":"FATE INTERVENES destiny-level event life redirect","Parents":"powerful parental lineage"},
    "tian_ji":{"Life":"analytical mind restless intelligence","Siblings":"clever peers intellectual competition","Spouse":"intellectual partnership","Children":"intelligent offspring","Wealth":"calculated financial moves money through intelligence","Health":"nervous system sensitivity overthinking affects body","Travel":"planned journeys strategic relocation","Friends":"strategic alliances","Career":"strategic moves advisor consultant","Property":"strategic real estate","Fortune":"luck through calculation","Parents":"analytical education-focused upbringing"},
    "tai_yang":{"Life":"radiant generous public figure","Siblings":"protector among peers","Spouse":"generous partner gives too much away","Children":"proud of offspring public eye","Wealth":"public-facing income generosity paradox","Health":"eye issues heart burnout from giving","Travel":"purposeful outward movement","Friends":"generous known in wide circles","Career":"public recognition visible career","Property":"prominent residence","Fortune":"luck through visibility and service","Parents":"strong father patriarchal influence"},
    "wu_qu":{"Life":"disciplined financially driven tough exterior","Siblings":"competitive peers financial arena","Spouse":"financially practical money-driven union","Children":"disciplined offspring strict parenting","Wealth":"strong earning through discipline military precision","Health":"respiratory issues strong but brittle","Travel":"business trips purposeful","Friends":"wealth through connections with effort","Career":"finance military law enforcement","Property":"strategic acquisition real estate as vehicle","Fortune":"luck through hard work","Parents":"financially strict military upbringing"},
    "tian_tong":{"Life":"easygoing comfort-seeking youthful","Siblings":"peaceful non-competitive","Spouse":"harmonious comfort-focused union","Children":"easygoing playful parent","Wealth":"passive income easy money","Health":"good but overindulgence risk","Travel":"leisure comfort-seeking","Friends":"harmonious pleasure-oriented","Career":"low-stress service hospitality","Property":"comfortable pleasant home","Fortune":"luck in leisure blessings through relaxation","Parents":"gentle upbringing comfort provided"},
    "lian_zhen":{"Life":"complex intense charming but guarded","Siblings":"intense purity standards","Spouse":"intense passionate jealousy possible","Children":"intense creative complex relationship","Wealth":"complex money wealth through intensity","Health":"heart fire emotional intensity affects body","Travel":"intense journeys complication","Friends":"intense loyalty demands","Career":"passionate politics law entertainment","Property":"property with history renovation","Fortune":"complicated luck strings attached","Parents":"complex intensity from upbringing"},
    "tian_fu":{"Life":"stable wealth-attracting conservative reliable","Siblings":"prosperous financial cooperation","Spouse":"wealthy stable partner marriage as vault","Children":"providing abundantly legacy investment","Wealth":"VAULT OPENS structured accumulation security achieved","Health":"stable stomach focus over-accumulation","Travel":"comfortable well-funded wealthier area","Friends":"wealthy financial network resources","Career":"banking finance treasury management","Property":"prime real estate valuable holdings portfolio","Fortune":"stored blessings released karma pays off","Parents":"financially stable family wealth"},
    "tai_yin":{"Life":"emotionally rich intuitive fragile","Siblings":"emotionally bonded sensitive","Spouse":"deeply emotional sensitive spouse","Children":"emotionally attuned artistic offspring","Wealth":"real estate female industries gradual","Health":"emotional affects body sleep hormonal","Travel":"internal journeys emotional relocations","Friends":"emotionally deep female allies","Career":"behind-scenes night work artistic","Property":"beautiful home female connections","Fortune":"luck through patience gradual","Parents":"strong maternal influence shaped by mother"},
    "tan_lang":{"Life":"charismatic multi-talented magnetic restless","Siblings":"competitive charisma social dominance","Spouse":"passionate infidelity risk magnetic partner","Children":"creative talented many interests","Wealth":"charm and hustle multiple streams","Health":"liver reproductive excess illness","Travel":"restless hungry for movement","Friends":"socially magnetic wide shallow","Career":"entertainment sales marketing charisma","Property":"multiple properties frequent moves","Fortune":"luck through desire appetite attracts","Parents":"desire-driven strong appetites"},
    "ju_men":{"Life":"sharp communicator argumentative","Siblings":"verbal competition debate","Spouse":"argumentative verbal conflict","Children":"talkative argumentative offspring","Wealth":"money through speech law consulting","Health":"throat mouth digestive stress","Travel":"disputes barriers abroad","Friends":"arguments disputes about value","Career":"lawyer debater critic teacher","Property":"disputes legal issues real estate","Fortune":"luck through speech problems through speech","Parents":"critical verbal discipline argumentative"},
    "tian_xiang":{"Life":"service-oriented helpful diplomatic","Siblings":"supportive helpful among equals","Spouse":"supportive helper-partner dynamic","Children":"nurturing service-oriented offspring","Wealth":"wealth through service administrative","Health":"stable issues from overwork","Travel":"service-related helping others","Friends":"helpful mutual support","Career":"support administration advisor","Property":"comfortable functional not ostentatious","Fortune":"luck through helping service rewarded","Parents":"supportive service-oriented"},
    "tian_liang":{"Life":"old soul wise protective","Siblings":"elder protective role","Spouse":"older wiser protected marriage","Children":"protective sheltering offspring","Wealth":"conservative management protected assets","Health":"longevity recovery elder care","Travel":"protected guided pilgrimage","Friends":"elder mentors wise connections","Career":"government medicine religion protective","Property":"inherited protected property","Fortune":"protected by fate disasters averted elders","Parents":"strong grandparental sheltered childhood"},
    "qi_sha":{"Life":"warrior intense feared respected","Siblings":"fierce competition survival","Spouse":"intense power struggle transformative","Children":"difficult birth children of intensity","Wealth":"volatile risk/reward military wealth","Health":"injury surgery acute illness accident","Travel":"dangerous military crisis relocation","Friends":"powerful dangerous competitive","Career":"military surgery demolition reform crisis","Property":"demolition renovation seized assets","Fortune":"FATE PIVOT through destruction makes room for destiny","Parents":"harsh military discipline absent authority"},
    "po_jun":{"Life":"revolutionary constant reinvention pioneer","Siblings":"peer groups shattered revolutionary","Spouse":"partnership demolished rebuilt revolutionary","Children":"unconventional break molds","Wealth":"boom-bust breaking and rebuilding","Health":"crisis and recovery cycles","Travel":"dramatic relocations permanent departures","Friends":"dissolve and reform revolutionary","Career":"career reinvention startup demolition restructuring","Property":"renovation flipping through destruction","Fortune":"dramatic fate shifts luck through upheaval","Parents":"broke from tradition unconventional"},
}

KEYWORD_MAP = {
    "wealth":["wealth","money","financial","vault","earning","assets","income","accumulation"],
    "partnership":["partnership","marriage","spouse","union","alliance","partner"],
    "destruction":["demolish","destroy","break","revolution","shatter","demolished"],
    "career":["career","public","authority","recognition","profession","executive"],
    "health":["health","body","illness","vitality","emotional","injury","surgery"],
    "property":["property","real estate","home","housing","residence","renovation"],
    "transformation":["transformation","rebirth","phoenix","crisis","reinvention"],
    "isolation":["isolation","withdrawal","hidden","secret","alone"],
    "children":["children","offspring","creative","legacy","production"],
    "conflict":["conflict","argument","dispute","fight","confrontation","verbal"],
    "travel":["travel","movement","relocation","journey","departure"],
    "education":["education","learning","knowledge","study","philosophy"],
    "fate_pivot":["fate","destiny","pivot","redirect","intervene"],
    "restriction":["restrict","limit","block","deny","delay","tighten"],
    "recognition":["recognition","visible","spotlight","noticed","award","public"],
    "protection":["protect","shelter","shield","safety","guard","elder"],
}


# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def get_element_relation(acting: str, receiving: str) -> str:
    direct = ELEMENT_INTERACTIONS.get((acting, receiving))
    if direct:
        return direct
    reverse = ELEMENT_INTERACTIONS.get((receiving, acting))
    if reverse == "PRODUCES":
        return "PRODUCED_BY"
    elif reverse == "CONTROLS":
        return "CONTROLLED_BY"
    return "NEUTRAL"

def get_sign_sequence(starting_sign: str) -> list:
    idx = SIGN_ORDER.index(starting_sign)
    return SIGN_ORDER[idx:] + SIGN_ORDER[:idx]

def compute_year_stem_branch(year: int) -> dict:
    offset = (year - 4) % 60
    stem = STEMS[offset % 10]
    branch = BRANCHES[offset % 12]
    return {"stem": stem, "branch": branch}

def extract_keywords(text: str) -> list:
    found = []
    text_lower = text.lower()
    for domain, triggers in KEYWORD_MAP.items():
        if any(t in text_lower for t in triggers):
            found.append(domain)
    return found


# ═══════════════════════════════════════════════════════════
# LAYER 1: NAYIN SOUL ELEMENT
# ═══════════════════════════════════════════════════════════

def compute_nayin_layer(nayin_data: dict, year: int) -> dict:
    """Compute nayin element interaction for a given year."""
    native_element = nayin_data.get("element", "METAL")
    nayin_pinyin = nayin_data.get("pinyin", "")
    props = NAYIN_PROPERTIES.get(nayin_pinyin, {})

    year_sb = compute_year_stem_branch(year)
    stem_element = year_sb["stem"]["element"]
    branch_element = year_sb["branch"]["element"]

    stem_relation = get_element_relation(stem_element, native_element)
    branch_relation = get_element_relation(branch_element, native_element)
    stem_score = INTERACTION_SCORES.get(stem_relation, 0)
    branch_score = INTERACTION_SCORES.get(branch_relation, 0)
    composite = (stem_score + branch_score) / 2

    # Check birth stem return
    birth_stem = nayin_data.get("birth_stem", "")
    birth_branch = nayin_data.get("birth_branch", "")
    stem_return = year_sb["stem"]["name"] == birth_stem
    branch_return = year_sb["branch"]["name"] == birth_branch

    return {
        "native_element": native_element,
        "native_nayin": nayin_data.get("english_name", ""),
        "nayin_pinyin": nayin_pinyin,
        "nayin_properties": props,
        "year_stem": year_sb["stem"]["name"],
        "year_branch": year_sb["branch"]["name"],
        "stem_element": stem_element,
        "branch_element": branch_element,
        "stem_relation": stem_relation,
        "branch_relation": branch_relation,
        "stem_score": stem_score,
        "branch_score": branch_score,
        "composite_support": composite,
        "birth_stem_return": stem_return,
        "birth_branch_return": branch_return,
        "jiazi_return": stem_return and branch_return,
    }


# ═══════════════════════════════════════════════════════════
def get_age_contextual_house_subject(house: int, age: int) -> str:
    '''
    Universal age-contextual remapping of house subjects.
    Reads age from computed life stage; applies to any chart.
    Returns the appropriate subject for a house activation given the person's age.
    '''
    # Age brackets
    if age <= 12:
        bracket = "child"
    elif age <= 17:
        bracket = "teen"
    elif age <= 25:
        bracket = "young_adult"
    elif age <= 39:
        bracket = "adult"
    elif age <= 59:
        bracket = "middle"
    else:
        bracket = "senior"

    # House subject by bracket
    remap = {
        1:  {"child": "child self-concept, body awareness", "teen": "identity formation", "young_adult": "self-identity", "adult": "self", "middle": "self", "senior": "self and legacy"},
        2:  {"child": "family financial situation affecting child", "teen": "first money, first job, values forming", "young_adult": "first earning, financial independence forming", "adult": "earnings and resources", "middle": "accumulated resources", "senior": "preservation of resources"},
        3:  {"child": "siblings/cousins, school, immediate environment", "teen": "peer communication, school, siblings", "young_adult": "peer network, learning, early mentors", "adult": "communication and siblings", "middle": "community of peers", "senior": "passing knowledge, communication"},
        4:  {"child": "family moves, home structure, caretakers", "teen": "home base stability or instability", "young_adult": "leaving home, first apartment", "adult": "home, family, real estate", "middle": "home as anchor for family", "senior": "ancestral home, final residence"},
        5:  {"child": "child's creative play, first crushes, joy", "teen": "creative identity, first romance, sports", "young_adult": "creative expression, dating, hobbies", "adult": "children, creativity, romance", "middle": "teens at home, creative legacy", "senior": "grandchildren, artistic legacy"},
        6:  {"child": "health events, school routine, body", "teen": "body changes, health, daily school", "young_adult": "body, illness, daily work routines", "adult": "health, daily work, service", "middle": "health management, chronic conditions", "senior": "health and daily routine"},
        7:  {"child": "parents' marriage/partnership, caretaker bond", "teen": "peer dynamics, early romance, best friend", "young_adult": "first serious partnership, committed relationship", "adult": "marriage, business partnership, rivals", "middle": "long marriage, committed alliances", "senior": "long partnership, widowhood"},
        8:  {"child": "family financial crisis or windfall, inherited issues", "teen": "first major loss or inherited family asset", "young_adult": "deep transformation, first real loss", "adult": "shared resources, inheritance, transformation", "middle": "inheritance events, major transitions", "senior": "estate, legacy transmission"},
        9:  {"child": "travel with family, religious/cultural exposure", "teen": "study abroad, faith questions, travel", "young_adult": "higher education, foreign travel", "adult": "philosophy, foreign matters, higher learning", "middle": "teaching, mentoring, pilgrimage", "senior": "wisdom, final journeys"},
        10: {"child": "parents' career, caretaker's public role", "teen": "school reputation, early ambitions", "young_adult": "first career steps, public identity forming", "adult": "career, public reputation, authority", "middle": "career peak or final pivot", "senior": "legacy, post-retirement contribution"},
        11: {"child": "friends, groups, social belonging", "teen": "peer group, clubs, social identity", "young_adult": "college friends, early network, hopes", "adult": "friends, professional network, community", "middle": "established network, mentees", "senior": "lifelong friends, community of elders"},
        12: {"child": "hidden family matters, fears, imagination", "teen": "hidden struggles, secrets, solitude", "young_adult": "spiritual seeking, hidden aspects", "adult": "isolation, secrets, hidden matters", "middle": "contemplation, withdrawal, legacy reflection", "senior": "endings, dissolution, transcendence"},
    }
    return remap.get(house, {}).get(bracket, "")


# LAYER 2: PROFECTION
# ═══════════════════════════════════════════════════════════

def compute_profection(age: int, hellenistic: dict) -> dict:
    """Compute annual profection from Hellenistic chart data."""
    asc_sign = hellenistic.get("ascendant", {}).get("sign", "Libra")
    planets = hellenistic.get("planets", [])

    house_number = (age % 12) + 1
    signs = get_sign_sequence(asc_sign)
    profected_sign = signs[house_number - 1]
    lord_planet = TRADITIONAL_RULERS.get(profected_sign, "Venus")

    # Find lord in planets
    lord_data = None
    for p in planets:
        if p.get("name", "").lower() == lord_planet.lower():
            lord_data = p
            break

    if not lord_data:
        lord_data = {"name": lord_planet, "sign": "unknown", "house": 1, "dignity": "peregrine", "is_retrograde": False}

    dignity = lord_data.get("dignity", "peregrine").lower()
    dignity_info = DIGNITY_SCORES.get(dignity, DIGNITY_SCORES["peregrine"])
    lord_house = lord_data.get("house", 1)

    return {
        "house": house_number,
        "sign": profected_sign,
        "lord": lord_planet,
        "lord_sign": lord_data.get("sign", "unknown"),
        "lord_house": lord_house,
        "lord_dignity": dignity,
        "lord_retrograde": lord_data.get("is_retrograde", False),
        "house_themes": HOUSE_THEMES.get(house_number, HOUSE_THEMES[1]),
        "lord_house_themes": HOUSE_THEMES.get(lord_house, HOUSE_THEMES[1]),
        "dignity_score": dignity_info["score"],
        "dignity_effect": dignity_info["effect"],
    }


# ═══════════════════════════════════════════════════════════
# LAYER 3: ASPECT ACTIVATION
# ═══════════════════════════════════════════════════════════

ASPECT_MEANINGS = {
    "conjunction":"fused_energy_amplification",
    "sextile":"opportunity_cooperation",
    "square":"tension_conflict_forced_action",
    "trine":"natural_flow_support_ease",
    "opposition":"polarity_confrontation_projection",
}

def compute_activated_aspects(profection: dict, hellenistic: dict) -> list:
    """Find aspects activated by the profection lord."""
    lord = profection["lord"].lower()
    aspects = hellenistic.get("aspects", [])
    planets = hellenistic.get("planets", [])
    sect_light = hellenistic.get("sect_light", "").lower()
    activated = []

    planet_map = {p.get("name","").lower(): p for p in planets}

    for asp in aspects:
        p1 = asp.get("planet_1", asp.get("planet1", "")).lower()
        p2 = asp.get("planet_2", asp.get("planet2", "")).lower()
        asp_type = asp.get("type", asp.get("aspect_type", "")).lower()
        orb = asp.get("orb", 10.0)

        if lord in [p1, p2] and orb <= 3.0:
            other = p2 if p1 == lord else p1
            other_data = planet_map.get(other, {})
            strength = 1.0 / (1.0 + orb)

            activated.append({
                "other_planet": other.title(),
                "aspect_type": asp_type,
                "orb": orb,
                "strength": round(strength, 3),
                "other_house": other_data.get("house", 0),
                "other_dignity": other_data.get("dignity", "peregrine"),
                "meaning": ASPECT_MEANINGS.get(asp_type, "unknown"),
                "is_sect_light": other.lower() == sect_light,
            })

    return sorted(activated, key=lambda a: a["strength"], reverse=True)


# ═══════════════════════════════════════════════════════════
# LAYER 4: ANNUAL PALACE + STARS
# ═══════════════════════════════════════════════════════════

def compute_annual_palace(year: int, zwds: dict, birth_year: int) -> dict:
    """Find the ZWDS annual palace for a given year."""
    annuals = zwds.get("annuals", [])
    age = year - birth_year

    for a in annuals:
        if a.get("age") == age or a.get("year") == year:
            palace_name = a.get("palace_name_english", "")
            # Parse stars - pinyin is reliable (underscore-separated names, space between stars)
            stars_pinyin_raw = a.get("stars", "")
            if isinstance(stars_pinyin_raw, str):
                pinyin_list = [s.strip() for s in stars_pinyin_raw.split() if s.strip()]
            else:
                pinyin_list = stars_pinyin_raw if stars_pinyin_raw else []

            # Map pinyin to English from our star database
            PINYIN_TO_ENGLISH = {k: v.get("Life","").split(",")[0].strip() for k,v in STAR_PALACE_EFFECTS.items()}
            PINYIN_TO_ENGLISH.update({"zi_wei":"Purple Star Emperor","tian_ji":"Heavenly Mechanism","tai_yang":"Sun",
                "wu_qu":"Military Wealth","tian_tong":"Heavenly Unity","lian_zhen":"Chastity",
                "tian_fu":"Celestial Vault","tai_yin":"Moon","tan_lang":"Greedy Wolf",
                "ju_men":"Giant Gate","tian_xiang":"Heavenly Minister","tian_liang":"Celestial Beam",
                "qi_sha":"Seven Killings","po_jun":"Army Breaker"})
            star_list = [PINYIN_TO_ENGLISH.get(sp, sp) for sp in pinyin_list]

            # Get star-palace specific effects (age-aware only - no fallback to generic)
            star_effects = []
            for sp in pinyin_list:
                age_effect = get_star_palace_age_effect(sp, palace_name, age)
                if age_effect:
                    star_effects.append({"star": sp, "palace": palace_name, "effect": age_effect, "age_bracket": get_age_bracket(age)})

            return {
                "year": year,
                "age": age,
                "palace_name": palace_name,
                "palace_branch": a.get("palace_branch", ""),
                "year_stem_branch": a.get("year_stem_branch", ""),
                "stars_english": star_list,
                "stars_pinyin": pinyin_list,
                "star_palace_effects": star_effects,
                "palace_themes": PALACE_THEMES.get(palace_name, {}),
                "is_empty": len(pinyin_list) == 0,
            }

    return {"year": year, "age": age, "palace_name": "", "stars_english": [], "star_palace_effects": [], "palace_themes": {}, "is_empty": True}


# ═══════════════════════════════════════════════════════════
# LAYER 5: DECADE PALACE
# ═══════════════════════════════════════════════════════════

def compute_decade_palace(age: int, zwds: dict) -> dict:
    """Find the ZWDS decade palace for a given age."""
    decades = zwds.get("decades", [])

    for d in decades:
        start = d.get("start_age", 0)
        end = d.get("end_age", 0)
        if start <= age <= end:
            palace_name = d.get("palace_name_english", "")
            stars_pinyin_raw = d.get("stars", "")
            if isinstance(stars_pinyin_raw, str):
                pinyin_list = [s.strip() for s in stars_pinyin_raw.split() if s.strip()]
            else:
                pinyin_list = stars_pinyin_raw if stars_pinyin_raw else []

            PINYIN_TO_ENGLISH = {"zi_wei":"Purple Star Emperor","tian_ji":"Heavenly Mechanism","tai_yang":"Sun",
                "wu_qu":"Military Wealth","tian_tong":"Heavenly Unity","lian_zhen":"Chastity",
                "tian_fu":"Celestial Vault","tai_yin":"Moon","tan_lang":"Greedy Wolf",
                "ju_men":"Giant Gate","tian_xiang":"Heavenly Minister","tian_liang":"Celestial Beam",
                "qi_sha":"Seven Killings","po_jun":"Army Breaker"}
            star_list = [PINYIN_TO_ENGLISH.get(sp, sp) for sp in pinyin_list]

            star_effects = []
            for sp in pinyin_list:
                decade_midpoint = (start + end) // 2
                age_effect = get_star_palace_age_effect(sp, palace_name, decade_midpoint)
                if age_effect:
                    star_effects.append({"star": sp, "palace": palace_name, "effect": age_effect, "age_bracket": get_age_bracket(decade_midpoint)})

            return {
                "palace_name": palace_name,
                "palace_branch": d.get("palace_branch", ""),
                "start_age": start,
                "end_age": end,
                "stars_english": star_list,
                "stars_pinyin": pinyin_list,
                "star_palace_effects": star_effects,
                "palace_themes": PALACE_THEMES.get(palace_name, {}),
                "position": "TRANSITION_IN" if age == start else "TRANSITION_OUT" if age == end else "MID_DECADE",
            }

    return {"palace_name": "", "start_age": 0, "end_age": 0, "stars_english": [], "palace_themes": {}, "position": "UNKNOWN"}


# ═══════════════════════════════════════════════════════════
# LAYER 6: STEM-BRANCH YEAR
# ═══════════════════════════════════════════════════════════

def compute_stem_branch_layer(year: int, birth_stem: str, birth_branch: str, life_palace_branch: str) -> dict:
    year_sb = compute_year_stem_branch(year)
    stem = year_sb["stem"]
    branch = year_sb["branch"]

    internal = get_element_relation(stem["element"], branch["element"])

    # Life palace branch element
    life_elem = "FIRE"  # default
    for b in BRANCHES:
        if b["name"] == life_palace_branch:
            life_elem = b["element"]
            break

    branch_to_life = get_element_relation(branch["element"], life_elem)

    return {
        "stem": stem["name"],
        "branch": branch["name"],
        "stem_element": stem["element"],
        "branch_element": branch["element"],
        "internal_harmony": internal,
        "branch_to_life_palace": branch_to_life,
        "birth_stem_return": stem["name"] == birth_stem,
        "birth_branch_return": branch["name"] == birth_branch,
        "jiazi_return": stem["name"] == birth_stem and branch["name"] == birth_branch,
    }


# ═══════════════════════════════════════════════════════════
# LAYER 7: CYCLE PATTERN RECOGNITION
# ═══════════════════════════════════════════════════════════

def detect_cycles(age: int, history: dict) -> list:
    if age not in history:
        return []
    current = history[age]
    patterns = []

    # Lord return
    current_lord = current.get("profection", {}).get("lord", "")
    same_lord_ages = [a for a, d in history.items()
                      if d.get("profection", {}).get("lord") == current_lord and a < age]
    if same_lord_ages:
        cycle_num = len(same_lord_ages) + 1
        maturity = {1:"introduction",2:"adolescent",3:"adult",4:"mastery"}.get(cycle_num, "elder")
        patterns.append({"type":"LORD_RETURN","lord":current_lord,"previous_ages":same_lord_ages,
                         "cycle_number":cycle_num,"maturity":maturity})

    # Consecutive lord
    if age > 0 and (age - 1) in history:
        prev_lord = history[age - 1].get("profection", {}).get("lord", "")
        if prev_lord == current_lord:
            patterns.append({"type":"CONSECUTIVE_LORD","lord":current_lord})

    # Annual meets decade
    annual_palace = current.get("annual", {}).get("palace_name", "")
    decade_palace = current.get("decade", {}).get("palace_name", "")
    if annual_palace and annual_palace == decade_palace:
        patterns.append({"type":"ANNUAL_MEETS_DECADE","palace":annual_palace})

    # Decade transition + profection reset
    if current.get("decade", {}).get("position") == "TRANSITION_IN" and current.get("profection", {}).get("house") == 1:
        patterns.append({"type":"DOUBLE_RESET"})

    return patterns


# ═══════════════════════════════════════════════════════════
# CONVERGENCE SCORER
# ═══════════════════════════════════════════════════════════

def score_convergence(year_data: dict) -> dict:
    domain_scores = defaultdict(lambda: {"score": 0.0, "sources": []})

    prof = year_data.get("profection", {})
    # Profection house keywords
    for kw in prof.get("house_themes", {}).get("keywords", []):
        domain_scores[kw]["score"] += 0.30
        domain_scores[kw]["sources"].append("profection_house")

    # Lord natal house keywords
    for kw in prof.get("lord_house_themes", {}).get("keywords", []):
        domain_scores[kw]["score"] += 0.20
        domain_scores[kw]["sources"].append("lord_natal_house")

    # Dignity modifier - exalted/domicile lords deliver strongly; fallen/detriment lords frustrate hard.
    # These effects used to be +/- 0.15 which was too quiet. Raised so they surface as dominant themes.
    dig_score = prof.get("dignity_score", 0.15)
    dig_label = prof.get("lord_dignity", "peregrine").lower()

    # Strength multiplier: exaltation (1.0) > domicile (0.9) > peregrine (0.15) > fall (0.1) > detriment (0.05)
    if dig_label == "exaltation":
        strong_weight = 0.50  # +0.50 to each house theme domain, across all keywords
    elif dig_label == "domicile":
        strong_weight = 0.40
    elif dig_label in ("fall", "detriment"):
        strong_weight = 0  # handled as frustration below
    else:
        strong_weight = 0

    # Dignity adds weight AND a valence tag onto the EXISTING domain keywords (not a new keyword).
    # This lets multi-source bonuses stack — same "partnerships" gets hit by profection + lord_house + dignity + stars + aspects.
    if dig_label in ("exaltation", "domicile"):
        for kw in prof.get("house_themes", {}).get("keywords", []):
            domain_scores[kw]["score"] += strong_weight
            domain_scores[kw]["sources"].append(f"lord_{dig_label}")
            domain_scores[kw]["valence_tags"] = domain_scores[kw].get("valence_tags", []) + ["delivered"]
        # Lord also projects its natal house themes with strength
        for kw in prof.get("lord_house_themes", {}).get("keywords", []):
            domain_scores[kw]["score"] += strong_weight * 0.7
            domain_scores[kw]["sources"].append(f"lord_{dig_label}_in_house")
            domain_scores[kw]["valence_tags"] = domain_scores[kw].get("valence_tags", []) + ["active"]

    elif dig_label in ("fall", "detriment"):
        frustrate_weight = 0.45 if dig_label == "detriment" else 0.35
        for kw in prof.get("house_themes", {}).get("keywords", []):
            domain_scores[kw]["score"] += frustrate_weight
            domain_scores[kw]["sources"].append(f"lord_{dig_label}")
            domain_scores[kw]["valence_tags"] = domain_scores[kw].get("valence_tags", []) + ["frustrated"]
        # Fallen lord drags its natal house themes too
        for kw in prof.get("lord_house_themes", {}).get("keywords", []):
            domain_scores[kw]["score"] += frustrate_weight * 0.7
            domain_scores[kw]["sources"].append(f"lord_{dig_label}_in_house")
            domain_scores[kw]["valence_tags"] = domain_scores[kw].get("valence_tags", []) + ["strained"]

    # Decade palace
    decade = year_data.get("decade", {})
    for kw in decade.get("palace_themes", {}).get("keywords", []):
        domain_scores[kw]["score"] += 0.25
        domain_scores[kw]["sources"].append("decade_palace")

    # Decade star effects
    for se in decade.get("star_palace_effects", []):
        for kw in extract_keywords(se.get("effect", "")):
            domain_scores[kw]["score"] += 0.10
            domain_scores[kw]["sources"].append(f"decade_star_{se.get('star','')}")

    # Annual palace
    annual = year_data.get("annual", {})
    for kw in annual.get("palace_themes", {}).get("keywords", []):
        domain_scores[kw]["score"] += 0.20
        domain_scores[kw]["sources"].append("annual_palace")

    # Star-palace effects (most specific)
    for se in annual.get("star_palace_effects", []):
        for kw in extract_keywords(se.get("effect", "")):
            domain_scores[kw]["score"] += 0.25
            domain_scores[kw]["sources"].append(f"star_palace_{se.get('star','')}")

    # Nayin support
    nayin = year_data.get("nayin", {})
    support = nayin.get("composite_support", 0)
    if support > 0.3:
        domain_scores["resilience"]["score"] += support * 0.15
        domain_scores["resilience"]["sources"].append("nayin_support")
    elif support < -0.3:
        domain_scores["pressure"]["score"] += abs(support) * 0.15
        domain_scores["pressure"]["sources"].append("nayin_hostile")

    # Aspect activations
    for asp in year_data.get("aspects", []):
        orb = asp.get("orb", 10)
        asp_type = asp.get("aspect_type", "")
        is_sect = asp.get("is_sect_light", False)

        # Tight-orb amplifier: sub-0.5 degree orbs are exact and carry major weight
        if orb < 0.5:
            tightness_multiplier = 2.5  # near-exact = 2.5x normal
        elif orb < 1.0:
            tightness_multiplier = 1.8
        elif orb < 2.0:
            tightness_multiplier = 1.3
        else:
            tightness_multiplier = 1.0

        # Sect light involvement - scale with tightness
        if is_sect:
            sect_score = 0.30 * tightness_multiplier
            domain_scores["significance"]["score"] += sect_score
            domain_scores["significance"]["sources"].append("sect_light")
            # Very tight aspects to sect light = headline event
            if orb < 0.5:
                domain_scores["major_event"]["score"] += 0.40
                domain_scores["major_event"]["sources"].append("exact_sect_light_aspect")

        # Tight conjunction of any planet
        if asp_type == "conjunction" and orb < 1.0:
            domain_scores["intensity"]["score"] += 0.20 * tightness_multiplier
            domain_scores["intensity"]["sources"].append("tight_conjunction")

        # Tight hard aspect (square/opposition) carries crisis weight
        if asp_type in ("square", "opposition") and orb < 1.0:
            domain_scores["crisis_pressure"]["score"] += 0.25 * tightness_multiplier
            domain_scores["crisis_pressure"]["sources"].append(f"tight_{asp_type}")

        # Tight supportive aspect (trine/sextile) carries blessing weight
        if asp_type in ("trine", "sextile") and orb < 1.0:
            domain_scores["support_arriving"]["score"] += 0.20 * tightness_multiplier
            domain_scores["support_arriving"]["sources"].append(f"tight_{asp_type}")

    # Cycle patterns
    for pat in year_data.get("cycles", []):
        if pat["type"] == "DOUBLE_RESET":
            domain_scores["major_transition"]["score"] += 0.40
            domain_scores["major_transition"]["sources"].append("double_reset")
        elif pat["type"] == "ANNUAL_MEETS_DECADE":
            palace = pat.get("palace", "")
            for kw in PALACE_THEMES.get(palace, {}).get("keywords", []):
                domain_scores[kw]["score"] += 0.30
                domain_scores[kw]["sources"].append("annual_meets_decade")

    # Multi-source bonus - steeper curve so stacked signals compound hard, not linearly.
    for domain, data in domain_scores.items():
        unique = len(set(data["sources"]))
        if unique == 3:
            data["score"] *= 1.30
            data["multi_source"] = True
        elif unique == 4:
            data["score"] *= 1.70
            data["multi_source"] = True
        elif unique >= 5:
            data["score"] *= 2.20
            data["multi_source"] = True

    # Compression year detection - count how many independent HIGH-confidence domains are firing
    # If 4+ independent domains cross the HIGH threshold, this is a stacked-event year.
    high_confidence_count = sum(
        1 for d, dat in domain_scores.items()
        if len(set(dat["sources"])) >= 3 and dat["score"] >= 0.5
    )
    compression_flag = high_confidence_count >= 4

    sorted_domains = sorted(domain_scores.items(), key=lambda x: -x[1]["score"])
    return {
        "top_domains": [{"domain": d[0], "score": round(d[1]["score"], 3),
                         "sources": len(set(d[1]["sources"])),
                         "confidence": "HIGH" if len(set(d[1]["sources"])) >= 3 else "MEDIUM" if len(set(d[1]["sources"])) >= 2 else "LOW"}
                        for d in sorted_domains[:8]],
        "high_confidence_count": high_confidence_count,
        "compression_year": compression_flag,
    }


# ═══════════════════════════════════════════════════════════
# LONGEVITY ESTIMATOR
# ═══════════════════════════════════════════════════════════

def estimate_longevity(hellenistic: dict, zwds: dict) -> int:
    """Estimate projected lifespan from both chart systems."""
    base = 78  # average baseline

    # ZWDS Health palace stars
    palaces = zwds.get("palaces", [])
    health_stars = []
    for p in palaces:
        if p.get("name_english") == "Health":
            stars = p.get("stars", [])
            if isinstance(stars, list):
                for s in stars:
                    if isinstance(s, dict):
                        health_stars.append(s.get("pinyin", ""))
                    elif isinstance(s, str):
                        health_stars.append(s)

    # Tian Liang in health = longevity boost
    if "tian_liang" in health_stars:
        base += 8
    # Qi Sha in health = risk
    if "qi_sha" in health_stars:
        base -= 5
    # Po Jun in health = crisis cycles
    if "po_jun" in health_stars:
        base -= 3

    # Nayin endurance
    nayin_pinyin = zwds.get("nayin", {}).get("pinyin", "")
    props = NAYIN_PROPERTIES.get(nayin_pinyin, {})
    if props.get("strength") == "enduring":
        base += 4
    elif props.get("strength") == "fragile":
        base -= 4

    # Hellenistic: 8th house ruler dignity
    planets = hellenistic.get("planets", [])
    asc_sign = hellenistic.get("ascendant", {}).get("sign", "Libra")
    signs = get_sign_sequence(asc_sign)
    eighth_sign = signs[7]
    eighth_ruler = TRADITIONAL_RULERS.get(eighth_sign, "Mars")

    for p in planets:
        if p.get("name", "").lower() == eighth_ruler.lower():
            dig = p.get("dignity", "peregrine").lower()
            if dig in ["domicile", "exaltation"]:
                base += 3  # strong 8th ruler = less destructive transformation
            elif dig in ["fall", "detriment"]:
                base -= 3

    # Sect light condition
    sect = hellenistic.get("sect", "night")
    sect_light_name = "Moon" if sect == "night" else "Sun"
    for p in planets:
        if p.get("name", "").lower() == sect_light_name.lower():
            dig = p.get("dignity", "peregrine").lower()
            if dig in ["domicile", "exaltation"]:
                base += 3
            elif dig in ["fall", "detriment"]:
                base -= 4

    return max(60, min(95, base))


# ═══════════════════════════════════════════════════════════
# LAYER 8: LLM PROMPT + CLAUDE CALL
# ═══════════════════════════════════════════════════════════

def build_llm_prompt(all_years: list, nayin_data: dict, longevity: int, user_stance: str = "") -> str:
    """Build ONE prompt: full interpretation engine + per-year signals."""

    engine_framework = f"""You are the Starlogic Prediction Engine. You receive pre-computed astrological signals and translate them into life predictions using the interpretation framework below. Follow it exactly.

═══ PERSON'S FOUNDATION ═══
Soul Element: {nayin_data.get('english_name', '')} ({nayin_data.get('element', '')})
Properties: visibility={nayin_data.get('properties', {}).get('visibility', '')}, strength={nayin_data.get('properties', {}).get('strength', '')}, recognition={nayin_data.get('properties', {}).get('recognition', '')}
Projected lifespan: {longevity} years.

{user_stance}

═══ LAYER 1: NAYIN — THE OPERATING SYSTEM (FOUNDATION) ═══
The nayin is NOT a modifier. It IS the foundation through which every prediction delivers.

Visibility types:
- hidden/buried/low/dim = results build unseen, surface later
- exposed/prominent/explosive/supreme = results immediately visible
- subtle/worn/surface = results show gradually through observation
- emerging/fruiting = results arrive at predictable moments

Strength types:
- enduring/rooted/load_bearing/vast = survives hostile years intact
- fragile/unstable/thin = hostile years cause real damage
- sharp/explosive/rushing/overwhelming = acts with force when triggered
- flowing/flexible/practical = adapts rather than resists
- latent/smoldering = waits, then activates suddenly

Recognition types:
- delayed_then_sudden = invisible compound progress, then breakthrough
- immediate_threat/unavoidable = instant visible impact
- earned/crafted = recognition comes through effort
- divine/cosmic/overwhelming = larger-than-life arrival
- overlooked/common/uncertain = often missed by others

Element Interaction (composite_support score):
- PRODUCES (+1.0): environment feeds you. Supportive year, external conditions favor growth.
- SAME (+0.8): environment resonates. Core self reinforced. Familiar territory.
- CONTROLLED_BY (+0.6): you control environment. Person shapes circumstances.
- NEUTRAL (0.0): no elemental interaction.
- PRODUCED_BY (-0.5): you feed environment. Giving more than receiving. Draining.
- CONTROLS (-0.8): environment attacks you. Hostile. External forces reshape you.

Thresholds:
- composite_support > 0.5 → favorable year, things flow
- composite_support 0 to 0.5 → mildly supportive
- composite_support -0.3 to 0 → mildly draining
- composite_support < -0.5 → hostile, resistance everywhere

BIRTH_STEM_RETURN = personal will reasserts this year
JIAZI_RETURN = 60-year cycle reset, complete life chapter reset

═══ LAYER 2: PROFECTION — THE LOUDEST ANNUAL TRIGGER ═══
The profected house tells you WHAT DOMAIN activates.
The lord's natal dignity tells you QUALITY of delivery.
The lord's natal house tells you which OTHER domain colors this year.

Dignity effects:
- EXALTATION (1.0) = delivers MORE than expected, peak performance
- DOMICILE (0.9) = functions naturally and powerfully
- TRIPLICITY (0.6) = supported but not dominant
- PEREGRINE (0.15) = wandering, unfocused, no inherent support
- FALL (0.1) = promises that disappoint, expansion that contracts
- DETRIMENT (0.05) = works against its nature, frustration

House themes (what domain is activated):
- H1 self/body/identity/appearance
- H2 money/possessions/earning/values
- H3 communication/siblings/learning/short_travel
- H4 home/family/father/real_estate/foundation
- H5 children/creativity/pleasure/romance/speculation
- H6 health/work/daily_routine/service/illness
- H7 partnerships/marriage/open_enemies/contracts
- H8 transformation/shared_resources/inheritance/hidden_wealth/death_rebirth
- H9 higher_education/travel/philosophy/legal/foreign
- H10 career/public_reputation/authority/achievement
- H11 friends/allies/community/networks/hopes
- H12 isolation/hidden_enemies/self_undoing/endings/secrets

Derivation: "H{{profection}} activated, lord in H{{lord_house}} = {{house_themes}} colored by {{lord_house_themes}}, delivered at {{dignity_quality}}."

═══ LAYER 3: ASPECT ACTIVATION (BROADCAST SIGNALS) ═══
When the profection lord has tight natal aspects (orb under 3°), those aspects FIRE this year.
Tighter orb = stronger signal. Sect light involvement = disproportionate significance.

Aspect meanings:
- CONJUNCTION: fused energy, amplification, planets function as one
- SQUARE: tension, conflict, forced action, crisis
- TRINE: natural flow, support, ease, talent expressed
- SEXTILE: opportunity, cooperation, moderate support
- OPPOSITION: polarity, confrontation, projection onto others

When sect light is activated, the year carries MAJOR weight.

=== TIGHTNESS INDICATES MAGNITUDE, NOT VALENCE ===
A near-exact aspect (orb under 0.5 degrees) means the event is LARGE, not that it is GOOD or BAD.
- A tight square CAN be a profound positive event (first love, breakthrough committed to through effort)
- A tight trine CAN be a negative event (easy slide into loss, blessing that turns draining)
Valence comes from: nayin support direction, dignity of the planets involved, which age-contextual subject is activated, and the user's stance answers - NOT from aspect type alone.
When you see 'major_event' in convergence, translate it as defining year magnitude; then read the other signals to judge whether it felt good, hard, or mixed.

═══ LAYER 4: ANNUAL PALACE + STARS (FOREGROUND EVENT) ═══
The annual palace is WHAT specifically happens. Stars in that palace are the SPECIFIC manifestation.
Star-in-palace effects are the MOST SPECIFIC signal available. Trust them as the primary event prediction.

IMPORTANT: The EFFECTS strings you receive below are ALREADY age-calibrated to this person's age bracket
(Child 0-12, Teen 13-19, Adult 20-39, Middle 40-59, Senior 60+). Do not re-translate them for age.
They already reference age-appropriate events (school, career, health, family roles) for this specific year.
Use them as close to literal predictions, passed through the nayin lens for delivery style.

Examples of age-calibrated star-palace specificity:
- Po Jun in Travel at age 5 = "family relocations dramatic — cross-country, international, major uproot"
- Po Jun in Travel at age 25 = "permanent departures — leaves home country, cuts ties, doesn't return"
- Wu Qu in Career at age 42 = "CFO, director of operations, military officer rank, senior engineer"
- Qi Sha in Fortune at age 30 = "the year things break open — job loss leads to real calling, health scare forces priority reset"
- Zi Wei in Life at age 50 = "reaches peak authority — CEO, director, head of institution; commands full professional weight"
- Tian Fu in Wealth at age 38 = "peak accumulation years — investments grow, assets compound, net worth crosses thresholds"

Empty palace = themes present but without strong specific expression.
Missing effect for an age-palace combo = that combination doesn't apply at this life stage (skip it rather than force it).

=== QI SHA / PO JUN HAVE THREE MODES ===
Do not default to destructive interpretation. Choose the mode by reading the signals:
- PASSIVE DESTRUCTION (things happen to the person: fire, accident, layoff, diagnosis, loss): use when nayin support is negative, destruction-timing stance is FALSE (unresolved rupture ahead), or age is Child/Senior.
- ACTIVE DEMOLITION (the person chooses to break things: quit, divorce, sell, end an era): use when destruction-timing stance is TRUE (person already survived rupture), nayin is moderate to supportive, adult ages.
- AGGRESSIVE ACQUISITION (the person USES the destructive energy to build, scale, take over, compound hard): use when Tian Fu or Wu Qu is prominent in the chart, appetite/discipline stance favors building, and it is an Adult or Middle year.

Default to ACTIVE DEMOLITION (person as agent) when in doubt, not PASSIVE DESTRUCTION.

=== COMPRESSION YEARS ===
When a year has 4 or more independent HIGH-confidence convergence signals firing, flag it as a COMPRESSION YEAR.
A compression year stacks multiple independent major events in a single 12-month span: a career change AND a relationship event AND a property event AND a health event all hitting together.
Do not average them into one vague theme. Predict each one explicitly as its own event, and name the year as "a year that carries several of your life's biggest events at once."

=== NAYIN AS TIMING, NOT JUST FLAVOR ===
The nayin visibility property is a TIMING instruction:
- hidden / buried / low / dim nayin = events build invisibly over years, then surface as sudden breakthroughs. A "seed year" may feel small but germinates into a surface event 10 to 20 years later. When describing a hidden-nayin person's young-adult years, frame them as "the seed of what will surface later" rather than as the climax.
- exposed / prominent / explosive nayin = events and visibility land in the same year. The signal IS the event.
- subtle / worn / crafted nayin = results emerge through observation over months, not years.
- emerging / fruiting nayin = events arrive at predictable harvest moments (major palace cycles, decade transitions).

Read the person's nayin visibility first; it tells you WHEN to expect the signals to land, not just WHAT.

═══ LAYER 5: DECADE PALACE (BACKGROUND THEME) ═══
Sets the ~10-year backdrop. Every year within plays against this backdrop.
- TRANSITION_IN (first year) = decade energy arriving
- MID_DECADE = peak expression of decade theme
- TRANSITION_OUT (last year) = decade energy leaving, closing chapter

═══ LAYER 6: STEM-BRANCH ENVIRONMENT ═══
Year's elemental air. Modifies everything else.
- internal harmony PRODUCES/SAME = year has internal coherence
- internal harmony CONTROLS = year has internal tension
- branch_to_life_palace shows how year relates to core identity

═══ LAYER 7: CYCLE PATTERNS ═══
- LORD_RETURN: cycle_number 1=introduction, 2=adolescent_expression, 3=adult_mastery, 4=elder_wisdom
- CONSECUTIVE_LORD: prolonged single influence, malefic double = extended trial, benefic double = extended blessing
- ANNUAL_MEETS_DECADE: DOUBLE ACTIVATION, peak intensity for that domain in entire decade
- DOUBLE_RESET: decade + profection reset simultaneously = major life chapter change

═══ CONVERGENCE CONFIDENCE ═══
HIGH (3+ layer sources): bold specific prediction, this WILL happen
MEDIUM (2 sources): moderate claim, likely theme
LOW (1 source): mild/background, mention only if it fits the narrative
Conflicting signals: the TENSION itself is the prediction

=== DOMAIN LABEL SEMANTICS ===
When you see these suffixes in the CONVERGENCE line, they modify how you describe the event:
- <domain>_delivered = profection lord exalted/domicile on this domain -- predict CLEAN SUCCESS, opportunity landing, achievement
- <domain>_active = lord's natal house domain also activating -- secondary theme woven into primary
- <domain>_frustrated = profection lord fallen/detriment -- predict BLOCKED, almost-wins, frustration in this domain
- <domain>_strained = lord's natal house domain dragged down by weak lord -- secondary strain theme
- major_event = tight aspect to sect light under 0.5 degrees -- this is a HEADLINE year, a defining event
- crisis_pressure = tight square/opposition under 1 degree -- predict confrontation, forced action, rupture
- support_arriving = tight trine/sextile under 1 degree -- predict help, opportunity, mentor, breakthrough support

═══ AGE-APPROPRIATE LANGUAGE (SECONDARY GUIDE) ═══
The star-palace EFFECTS above are already age-calibrated. This guide is only for non-star-palace signals
(profection house themes, nayin support, aspects) which need age translation:
- Child (0-12): family events, school, peer dynamics, parent's circumstances affecting child
- Teen (13-19): identity formation, peer relationships, school transitions, first independence
- Adult (20-39): education, career building, marriage, first property, first children
- Middle (40-59): career peak or pivot, teens at home, partnership maturity, legacy thinking
- Senior (60+): consolidation, health focus, mentorship, wealth preservation, meaning-making

═══ OUTPUT RULES ═══
For EACH year:
- Exactly 3 bullets (4 max for HIGH convergence years with major events)
- Each bullet ONE sentence under 15 words
- SPECIFIC and FALSIFIABLE — testable against real events
- Use concrete nouns: "property purchase" not "material expansion", "job change" not "career transition"
- Never mention astrology terms, mechanics, layers, dignities, or signal codes
- Never say "you may", "could", "might" — make real predictions
- HIGH confidence + specific stars = bold concrete claims
- Deliver predictions through the person's nayin lens (hidden = invisible buildup, exposed = public events)

═══ YEAR-BY-YEAR SIGNALS (THE DATA) ═══
"""

    year_blocks = []
    for yd in all_years:
        age = yd["age"]
        year = yd["year"]
        prof = yd["profection"]
        nayin = yd["nayin"]
        annual = yd["annual"]
        decade = yd["decade"]
        aspects = yd["aspects"]
        stem_branch = yd["stem_branch"]
        cycles = yd.get("cycles", [])
        convergence = yd.get("convergence", {"top_domains": []})
        themes = yd.get("themes", [])
        compression_year = yd.get("compression_year", False)

        block = f"""
--- AGE {age} ({year}) ---
NAYIN: {nayin['stem_relation']}({nayin['stem_element']}→native) + {nayin['branch_relation']}({nayin['branch_element']}→native) = support:{nayin['composite_support']:.2f} {'BIRTH_STEM_RETURN' if nayin['birth_stem_return'] else ''} {'JIAZI_RETURN' if nayin.get('jiazi_return') else ''}
PROFECTION: H{prof['house']} ({prof['house_themes']['short']}) - age-contextual subject: {get_age_contextual_house_subject(prof['house'], age)} | Lord={prof['lord']} {prof['lord_dignity']}({prof['dignity_score']}) in H{prof['lord_house']} ({prof['lord_house_themes']['short']}) - lord-house subject: {get_age_contextual_house_subject(prof['lord_house'], age)} {'Rx' if prof.get('lord_retrograde') else ''}
ASPECTS FIRED: {'; '.join([f"{a['other_planet']} {a['aspect_type']} orb={a['orb']}° H{a['other_house']}" + (' SECT_LIGHT' if a.get('is_sect_light') else '') for a in aspects[:3]]) if aspects else 'none'}
ANNUAL: {annual.get('palace_name','')} [{', '.join(annual.get('stars_english',[]))}] EFFECTS (age-calibrated): {'; '.join([se['effect'] for se in annual.get('star_palace_effects',[])])}
DECADE: {decade.get('palace_name','')} [{', '.join(decade.get('stars_english',[]))}] {decade.get('position','')} EFFECTS (age-calibrated): {'; '.join([se['effect'] for se in decade.get('star_palace_effects',[])])}
STEM-BRANCH: {stem_branch['stem']} {stem_branch['branch']} internal={stem_branch['internal_harmony']} to_life={stem_branch['branch_to_life_palace']}
CYCLES: {'; '.join([f"{c['type']}{'='+c.get('palace','') if c.get('palace') else ''}{'='+c.get('maturity','') if c.get('maturity') else ''}" for c in cycles]) if cycles else 'none'}
THEMES (ZWDS-led, Hellenistic validates): {' | '.join([f"{t['theme']}[{t['confidence']}]" for t in themes[:5]]) if themes else 'no strong themes'}{' <<< COMPRESSION YEAR - 3+ themes at MEDIUM/HIGH' if compression_year else ''}
THEME EVIDENCE: {'; '.join([f"{t['theme']}: ZWDS={'/'.join(t['zwds_evidence'][:2])}; Hel={t['hellenistic_strength']}" for t in themes[:3]]) if themes else ''}"""
        year_blocks.append(block)

    footer = """

=== OUTPUT FORMAT - TWO PARTS ===

PART 1: PERSONALITY PORTRAIT (write these 8 sections first)

Write 8 sections, each beginning with a markdown H2 header exactly as shown below.
Each section is ~150-200 words of second-person prose (starts with "You..."). No jargon.
No references to "nayin", "sect", "benefic", "malefic", "palace", "Qi Sha", "Po Jun", "Tan Lang", "Wu Qu", "Zi Wei", "Tian Fu", "profection", or any astrological term.
Translate astrological concepts into plain human language the reader can feel.

Write in a grounded, honest, slightly reverent tone. Direct. No filler.
Use the 9 user stance answers above to TILT each section - if the chart suggests X but the user's stance confirms Y, trust the stance.

## Your Soul Element
Describe what their nayin IS (the image - gold in the sea, fire on a hilltop, etc.) and what kind of person this makes them at the foundational material level. How they are built. What this essence does in the world.

## Your Nature
Their temperament. How they move through the world. Day-born vs night-born expression. Rhythm of their internal life. How they process information and make decisions.

## Your Strengths
The 2-4 things their chart shows they are genuinely built to do well. Specific, not generic. Drawn from dignified placements and strong palace/star combinations.

## Your Shadows
The recurring patterns that trip them up. Blind spots. Where they struggle. Drawn from fallen/weak placements. Honest without being cruel.

## Your Relationships
How they show up in close bonds - romantic, familial, friendship. What they offer. What they struggle with. What kind of partner fits them best.

## Your Luck
Their overall luck flavor. Where fortune tends to land. Where it tends to slip. Protected / tested / rupture-prone / steady-builder / wealth-favored / relationally-favored - pick the archetype that fits this specific chart.

## Your Core Drive
What their life is fundamentally aimed at. The deeper mission their chart points to. What they are HERE to do.

## Your Timing
How their life unfolds. Hidden essence = invisible buildup, late bloom, seeds planted now surface in decades. Exposed essence = events and visibility land same-year. Describe their specific rhythm.

---

PART 2: YEAR-BY-YEAR TIMELINE (write all years AFTER the portrait, using this format)

**Age X (YYYY)**
- prediction
- prediction
- prediction

Generate predictions for EVERY year listed in the signals above. One sentence per bullet. Under 15 words each. Read the signals through the interpretation framework above - don't just restate the codes.

IMPORTANT: Write PART 1 first (all 8 portrait sections with ## headers), then write PART 2 (all year-by-year predictions). Do not mix them. Do not skip either part."""

    return engine_framework + "\n".join(year_blocks) + footer


# ═══════════════════════════════════════════════════════════
# MASTER ORCHESTRATOR
# ═══════════════════════════════════════════════════════════

async def run_prediction_engine(birth_data: dict, clarifying_answers: dict = None) -> dict:
    """Full pipeline: fetch charts → compute layers → score → return signals + prompt."""

    # Check cache (key includes clarifying answers so different answers produce different readings)
    cache_input = {"birth": birth_data, "answers": clarifying_answers or {}}
    cache_key = hashlib.md5(json.dumps(cache_input, sort_keys=True).encode()).hexdigest()
    if cache_key in READING_CACHE:
        return READING_CACHE[cache_key]

    # Fetch both engines
    async with httpx.AsyncClient(timeout=30.0) as client:
        hell_resp = await client.post(f"{HELLENISTIC_URL}/chart", json=birth_data)
        zwds_resp = await client.post(f"{ZWDS_URL}/chart", json=birth_data)

    if hell_resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Hellenistic engine error: {hell_resp.text}")
    if zwds_resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"ZWDS engine error: {zwds_resp.text}")

    hellenistic = hell_resp.json()
    zwds = zwds_resp.json()

    # Extract birth info
    birth_year = int(birth_data["birth_date"].split("-")[0])
    nayin_data = zwds.get("nayin", {})
    nayin_data["birth_stem"] = zwds.get("year_stem", "")
    nayin_data["birth_branch"] = zwds.get("year_branch", "")
    life_palace_branch = zwds.get("life_palace_branch", "Wu")

    # Estimate longevity
    longevity = estimate_longevity(hellenistic, zwds)
    end_age = longevity  # generate signals through projected lifespan

    # Compute all 7 layers for each year
    history = {}
    all_years = []

    for age in range(end_age + 1):
        year = birth_year + age

        nayin_layer = compute_nayin_layer(nayin_data, year)
        profection = compute_profection(age, hellenistic)
        aspects = compute_activated_aspects(profection, hellenistic)
        annual = compute_annual_palace(year, zwds, birth_year)
        decade = compute_decade_palace(age, zwds)
        stem_branch = compute_stem_branch_layer(year, nayin_data["birth_stem"], nayin_data["birth_branch"], life_palace_branch)

        year_data = {
            "age": age, "year": year,
            "nayin": nayin_layer, "profection": profection,
            "aspects": aspects, "annual": annual,
            "decade": decade, "stem_branch": stem_branch,
        }

        history[age] = year_data
        year_data["cycles"] = detect_cycles(age, history)
        year_data["convergence"] = score_convergence(year_data)
        # New theme-bridge layer: ZWDS-led themes validated by Hellenistic
        year_data["themes"] = build_year_themes(year_data, natal_palaces=zwds.get("palaces", []), natal_planets=hellenistic.get("planets", []))
        year_data["compression_year"] = is_compression_year(year_data["themes"])
        all_years.append(year_data)

    # Build LLM prompt (for Base44 InvokeLLM to use)
    questions = generate_clarifying_questions(nayin_data, hellenistic, zwds)
    user_stance = format_answers_for_llm(questions, clarifying_answers) if clarifying_answers else ""
    llm_prompt = build_llm_prompt(all_years, nayin_data, longevity, user_stance)

    result = {
        "birth_data": birth_data,
        "longevity_estimate": longevity,
        "nayin": nayin_data,
        "hellenistic_summary": {
            "ascendant": hellenistic.get("ascendant", {}),
            "sect": hellenistic.get("sect", ""),
            "planets": len(hellenistic.get("planets", [])),
        },
        "zwds_summary": {
            "life_palace": zwds.get("life_palace_branch", ""),
            "ju": f"{zwds.get('ju_element', '')} {zwds.get('ju_number', '')}",
        },
        "signals": all_years,
        "llm_prompt": llm_prompt,
    }

    READING_CACHE[cache_key] = result
    return result


# ═══════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════

class BirthInput(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone_offset: float
    clarifying_answers: Optional[dict] = None

@app.get("/health")
def health():
    return {"status": "ok", "engine": "prediction", "version": "1.0.0"}

@app.post("/clarifying_questions")
async def get_clarifying_questions(data: BirthInput):
    """Return 9 tailored true/false questions for this chart."""
    birth_data = data.model_dump()
    birth_data.pop("clarifying_answers", None)
    async with httpx.AsyncClient(timeout=30.0) as client:
        hell_resp = await client.post(f"{HELLENISTIC_URL}/chart", json=birth_data)
        zwds_resp = await client.post(f"{ZWDS_URL}/chart", json=birth_data)
    if hell_resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Hellenistic engine error: {hell_resp.text}")
    if zwds_resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"ZWDS engine error: {zwds_resp.text}")
    hellenistic = hell_resp.json()
    zwds = zwds_resp.json()
    nayin_data = zwds.get("nayin", {})
    questions = generate_clarifying_questions(nayin_data, hellenistic, zwds)
    return {"questions": questions, "count": len(questions)}

@app.post("/reading")
async def generate_reading(data: BirthInput):
    """Full life reading — ONE call, all layers, cached."""
    birth_data = data.model_dump()
    clarifying_answers = birth_data.pop("clarifying_answers", None)
    return await run_prediction_engine(birth_data, clarifying_answers)

@app.post("/reading/signals")
async def get_signals(data: BirthInput):
    """Raw layer outputs WITHOUT LLM — for debugging/validation."""
    birth_data = data.model_dump()

    async with httpx.AsyncClient(timeout=30.0) as client:
        hell_resp = await client.post(f"{HELLENISTIC_URL}/chart", json=birth_data)
        zwds_resp = await client.post(f"{ZWDS_URL}/chart", json=birth_data)

    hellenistic = hell_resp.json()
    zwds = zwds_resp.json()

    birth_year = int(birth_data["birth_date"].split("-")[0])
    nayin_data = zwds.get("nayin", {})
    nayin_data["birth_stem"] = zwds.get("year_stem", "")
    nayin_data["birth_branch"] = zwds.get("year_branch", "")
    life_palace_branch = zwds.get("life_palace_branch", "Wu")
    longevity = estimate_longevity(hellenistic, zwds)

    history = {}
    all_years = []
    for age in range(longevity + 1):
        year = birth_year + age
        year_data = {
            "age": age, "year": year,
            "nayin": compute_nayin_layer(nayin_data, year),
            "profection": compute_profection(age, hellenistic),
            "aspects": compute_activated_aspects(
                compute_profection(age, hellenistic), hellenistic),
            "annual": compute_annual_palace(year, zwds, birth_year),
            "decade": compute_decade_palace(age, zwds),
            "stem_branch": compute_stem_branch_layer(year, nayin_data["birth_stem"], nayin_data["birth_branch"], life_palace_branch),
        }
        history[age] = year_data
        year_data["cycles"] = detect_cycles(age, history)
        year_data["convergence"] = score_convergence(year_data)
        # New theme-bridge layer: ZWDS-led themes validated by Hellenistic
        year_data["themes"] = build_year_themes(year_data, natal_palaces=zwds.get("palaces", []), natal_planets=hellenistic.get("planets", []))
        year_data["compression_year"] = is_compression_year(year_data["themes"])
        all_years.append(year_data)

    return {"longevity": longevity, "signals": all_years}

@app.post("/longevity")
async def get_longevity(data: BirthInput):
    """Just the longevity estimate."""
    birth_data = data.model_dump()
    async with httpx.AsyncClient(timeout=30.0) as client:
        hell_resp = await client.post(f"{HELLENISTIC_URL}/chart", json=birth_data)
        zwds_resp = await client.post(f"{ZWDS_URL}/chart", json=birth_data)
    return {"longevity_estimate": estimate_longevity(hell_resp.json(), zwds_resp.json())}
