"""
Starlogic — Nayin Archetypes
30 unique Nayin variants for Q1 visibility + Q2 strength clarifying questions.

Each archetype is rooted in its specific symbolic character (Gold in the Sea,
Fire on the Mountain, Willow Wood, etc) and carries:
  - english: display name
  - element: element family
  - visibility_class: "compound" | "visible" | "mixed" — Q1 impact direction
  - strength_class:   "enduring" | "adaptive" | "balanced" — Q2 impact direction
  - visibility_statement: Q1 user-facing statement with TRUE/FALSE forks
  - strength_statement:   Q2 user-facing statement with TRUE/FALSE forks

Used by clarifying_questions.q1_nayin_visibility / q2_nayin_strength.
"""

NAYIN_ARCHETYPES = {
    "hai_zhong_jin": {
        "english": "Gold in the Sea",
        "element": "Metal",
        "visibility_class": "compound",
        "strength_class": "enduring",
        "visibility_statement": "Your value forms deep, slowly, where nobody sees — the way gold takes shape on the ocean floor. By the time anyone notices, you're already substantial. TRUE: I can build for years in silence without losing my drive. FALSE: Quiet building drains me — I need visible signs of progress.",
        "strength_statement": "When pressure comes, you absorb it fully and surface stronger later — the sea presses carbon into something denser. TRUE: Setbacks cut deep, then I come back denser than before. FALSE: I move on fast — I don't sit in things, I keep going.",
    },
    "lu_zhong_huo": {
        "english": "Fire in the Furnace",
        "element": "Fire",
        "visibility_class": "compound",
        "strength_class": "enduring",
        "visibility_statement": "Your energy operates inside a frame — disciplined, channeled, used to forge specific things. The fire serves the work. TRUE: I do best when my drive serves a clear purpose or container. FALSE: I work better with looser structure and freer expression.",
        "strength_statement": "Your pressure response is purposeful — you channel intensity into productive heat rather than letting it spread. TRUE: I run hot when there's something to forge. The pressure is the fuel. FALSE: When pushed, I don't make things — I withdraw or shut down.",
    },
    "da_lin_mu": {
        "english": "Timber of the Forest",
        "element": "Wood",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "Your presence is undeniable — you take up real space and the people around you know you're there. TRUE: I'm not subtle. My impact is visible to anyone who looks. FALSE: I'd rather work where my influence is felt than where it's seen.",
        "strength_statement": "Your roots run deep — you weather storms by holding ground, not by moving. The tree doesn't follow the wind. TRUE: I outlast things. I'm here for the long arc. FALSE: I change direction often. I don't get attached to plans that stop working.",
    },
    "lu_pang_tu": {
        "english": "Earth by the Road",
        "element": "Earth",
        "visibility_class": "compound",
        "strength_class": "enduring",
        "visibility_statement": "Your contribution is constant and largely overlooked — people walk on what you provide without thanking you. TRUE: I do the foundational work others miss. Recognition comes late if ever, and I'm okay with that. FALSE: I need to be seen for what I give. I won't stay invisible.",
        "strength_statement": "You bear what others put on you. The traffic of life packs you tighter over time. TRUE: I take what comes. I've been hardened by carrying weight. FALSE: I refuse to be the one everyone walks on. I push back.",
    },
    "jian_feng_jin": {
        "english": "Sword Blade Metal",
        "element": "Metal",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "Your edge is visible from a distance. People see you coming and either approach with respect or back away. TRUE: I'm sharp and people know it. I cut clean through what I deal with. FALSE: I'm softer than my chart says. The blade is more rumor than reality.",
        "strength_statement": "Your pressure response is precise — you cut through what's in the way rather than going around. TRUE: I move decisively when tested. I don't dull. FALSE: I freeze or bend under real pressure. The edge isn't always there.",
    },
    "shan_tou_huo": {
        "english": "Fire on the Mountain",
        "element": "Fire",
        "visibility_class": "visible",
        "strength_class": "adaptive",
        "visibility_statement": "Your fire shows from miles away. You don't get to be quiet. The mountain raises your flame. TRUE: I burn loud and people watch. The visibility is the point. FALSE: I'd rather work with smaller fires and less attention.",
        "strength_statement": "Your pressure response is wild — fast, expansive, sometimes hard to contain. TRUE: I move fast when tested. Sometimes too fast. FALSE: I've learned to constrain the wildness. It's mostly mastered now.",
    },
    "jian_xia_shui": {
        "english": "Water under the Stream",
        "element": "Water",
        "visibility_class": "compound",
        "strength_class": "adaptive",
        "visibility_statement": "Your work runs underground for a long time before it surfaces. The springs people see are downstream of effort nobody saw. TRUE: My current is mostly hidden. The visible parts are just where I broke ground. FALSE: I'd rather show my flow as I go than wait for it to break ground.",
        "strength_statement": "Your response to pressure is to keep flowing — never stuck, even when you can't see your way through. TRUE: I keep moving even when the path is invisible. Water finds its way. FALSE: I freeze when I can't see what's coming. The flow isn't automatic.",
    },
    "cheng_tou_tu": {
        "english": "Earth on the Wall",
        "element": "Earth",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "Your work protects what's inside. You're seen as structure, not spectacle. The wall is what people lean against. TRUE: I'm the foundation, the boundary, the one who holds things together. FALSE: I want to be inside the wall, not the wall itself.",
        "strength_statement": "Your pressure response is to hold the line — protect what's behind you, no matter what's pushing. TRUE: I don't let things through. I defend what matters. FALSE: I'd rather move with the pressure than block it.",
    },
    "bai_la_jin": {
        "english": "White Wax Metal",
        "element": "Metal",
        "visibility_class": "compound",
        "strength_class": "adaptive",
        "visibility_statement": "Your value is real but understated — refined, easy to miss at first glance. The fine detail is the value. TRUE: My quality shows on closer inspection. People who get me, really get me. FALSE: I make myself obvious. I don't wait for people to notice.",
        "strength_statement": "Your pressure response is to take new form — you reshape under heat rather than crack. TRUE: I adapt. I take whatever shape the work or moment requires. FALSE: I have a fixed form. Pressure doesn't reshape who I am.",
    },
    "yang_liu_mu": {
        "english": "Willow Wood",
        "element": "Wood",
        "visibility_class": "visible",
        "strength_class": "adaptive",
        "visibility_statement": "Your beauty is in how you move, not in your stillness. People notice your grace before they notice your structure. TRUE: I'm seen for how I move and adapt. FALSE: I'd rather be respected for what I hold than for how I bend.",
        "strength_statement": "Your pressure response is to bend, not break. The willow stays rooted while the branches sweep. TRUE: I let storms move me. I'm still here when they pass. FALSE: I stand firm. Bending feels like giving in.",
    },
    "quan_zhong_shui": {
        "english": "Spring Water",
        "element": "Water",
        "visibility_class": "mixed",
        "strength_class": "enduring",
        "visibility_statement": "Something fresh comes out of you all the time. People come to drink from your source. TRUE: I'm a wellspring — people draw from me without quite explaining how. FALSE: My source has been depleted. I don't have that endless freshness in me right now.",
        "strength_statement": "Your pressure response is to keep producing — even under load, the source doesn't dry. TRUE: I have something inside that keeps generating. I don't run out. FALSE: I run dry. I need replenishment from outside before I can give more.",
    },
    "wu_shang_tu": {
        "english": "Earth on the Roof",
        "element": "Earth",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "You hold a high, visible position — what you do shelters others below. The roof is what they see when they look up. TRUE: I'm the one others look up to or rely on from above. FALSE: I'd rather be on the ground, working alongside people, not over them.",
        "strength_statement": "Your pressure response is to hold weight — what's above you doesn't fall through. TRUE: I bear what people put on me. I don't collapse. FALSE: I push back on weight that isn't mine. I refuse to carry by default.",
    },
    "pi_li_huo": {
        "english": "Thunderbolt Fire",
        "element": "Fire",
        "visibility_class": "visible",
        "strength_class": "adaptive",
        "visibility_statement": "Your impact comes in sudden flashes — quiet, quiet, then everything changes at once. TRUE: My life has been a series of lightning strikes more than steady arcs. FALSE: My life has been steady growth. The dramatic strikes haven't been the pattern.",
        "strength_statement": "Your pressure response is explosive — you don't slow-build, you discharge. TRUE: I hold tension until it breaks. Then I move all at once. FALSE: I bleed pressure off steadily. No big discharges.",
    },
    "song_bai_mu": {
        "english": "Pine and Cypress Wood",
        "element": "Wood",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "You stay the same through all seasons. People know what they're getting. The evergreen doesn't change with the calendar. TRUE: My core hasn't changed in years. People can count on me. FALSE: I've changed more than people realize. The exterior is the same; the inside is different.",
        "strength_statement": "Your pressure response is to endure — outlast the cold without losing your nature. TRUE: I'm still me through the hardest years. FALSE: I've been reshaped by what I've been through. The original me isn't who's here now.",
    },
    "chang_liu_shui": {
        "english": "Long Flowing Water",
        "element": "Water",
        "visibility_class": "visible",
        "strength_class": "adaptive",
        "visibility_statement": "Your movement is constant and undeniable. The river doesn't stop. TRUE: I'm always moving toward something. People see the current. FALSE: I want stillness sometimes. The constant motion exhausts me.",
        "strength_statement": "Your pressure response is to keep going — water finds its way around what won't move. TRUE: I outlast obstacles by going around them. FALSE: I'd rather break through than flow around.",
    },
    "sha_zhong_jin": {
        "english": "Gold in the Sand",
        "element": "Metal",
        "visibility_class": "compound",
        "strength_class": "enduring",
        "visibility_statement": "Your real value is mixed with a lot of noise. It takes effort — yours or someone else's — to find. TRUE: Most of what surrounds me is filler. The gold is buried. FALSE: My value is obvious. I don't need anyone to dig for it.",
        "strength_statement": "Your pressure response is to require sifting — your real strength shows only after the noise is cleared. TRUE: I'm at my best after a lot has been stripped away. FALSE: My strength is on the surface. People don't have to dig to find it.",
    },
    "shan_xia_huo": {
        "english": "Fire at the Foot of the Mountain",
        "element": "Fire",
        "visibility_class": "compound",
        "strength_class": "enduring",
        "visibility_statement": "You burn quietly for a long time. The fire is low but it doesn't go out. TRUE: I work for years before anyone notices the heat. FALSE: I need visible flame or I lose interest in what I'm building.",
        "strength_statement": "Your pressure response is delayed ignition — you smolder, then catch. TRUE: I take a long time to fully engage. When I do, I'm hard to stop. FALSE: I engage fast. I don't have a long warm-up.",
    },
    "ping_di_mu": {
        "english": "Flat Land Wood",
        "element": "Wood",
        "visibility_class": "mixed",
        "strength_class": "adaptive",
        "visibility_statement": "Your impact is wide rather than tall — you cover ground that others don't bother with. TRUE: I do many things at modest scale. The reach is the point, not the height. FALSE: I'd rather build one great thing than many decent ones.",
        "strength_statement": "Your pressure response is to spread, not concentrate. TRUE: When pushed, I diversify. I don't fold one big thing. FALSE: I concentrate under pressure. I cut and protect what matters most.",
    },
    "bi_shang_tu": {
        "english": "Plastered Wall Earth",
        "element": "Earth",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "Your work is purpose-built — applied to specific needs, visible in the result. TRUE: I do specific jobs well. I don't do generic. FALSE: I work across many domains. I'm not narrow in what I do.",
        "strength_statement": "Your pressure response is to harden in place — the form you take is the form you keep. TRUE: I commit to what I am. Pressure cures me into shape. FALSE: I keep reshaping. Pressure doesn't fix my form.",
    },
    "jin_bo_jin": {
        "english": "Gold Foil Metal",
        "element": "Metal",
        "visibility_class": "visible",
        "strength_class": "adaptive",
        "visibility_statement": "Your value shows on the surface — bright, refined, but easily damaged if handled wrong. TRUE: I shine when I'm seen, and I need to be handled carefully. FALSE: I'm tougher than I look. I don't need careful handling.",
        "strength_statement": "Your pressure response is fragile — you can crack if pushed wrong, but in the right hands you're stunning. TRUE: I bend best in skilled hands. Rough use breaks me. FALSE: I'm rougher and more durable than my surface suggests.",
    },
    "fu_deng_huo": {
        "english": "Lamp Fire",
        "element": "Fire",
        "visibility_class": "compound",
        "strength_class": "adaptive",
        "visibility_statement": "Your fire is small and personal — bright in the right room, dim from far away. TRUE: I light up my own circle. Outside it, I'm easily missed. FALSE: I want broader reach. The intimate scale doesn't satisfy me.",
        "strength_statement": "Your pressure response is to need shelter — your fire needs the right conditions to stay lit. TRUE: I do best when people protect me from rough weather. FALSE: I weather any conditions. I don't need shelter.",
    },
    "tian_he_shui": {
        "english": "Heavenly River Water",
        "element": "Water",
        "visibility_class": "mixed",
        "strength_class": "enduring",
        "visibility_statement": "Your scope is bigger than what's in front of you — you operate at a level most people don't see daily. TRUE: My real concerns are bigger than the room I'm in. FALSE: I'm grounded in the immediate. The cosmic scope isn't where I live.",
        "strength_statement": "Your pressure response is vastness — you absorb and dissipate without losing yourself. TRUE: Most pressure feels small to me. I don't get knocked off course easily. FALSE: I feel small pressures big. The cosmic scale isn't actually where I sit.",
    },
    "da_yi_tu": {
        "english": "Great Earth of the Post Road",
        "element": "Earth",
        "visibility_class": "mixed",
        "strength_class": "enduring",
        "visibility_statement": "You're the foundation under what other people build. Foot traffic comes and goes; you stay. TRUE: I'm the long-arc base. Many people pass through what I hold up. FALSE: I want to be passing through, not being built on.",
        "strength_statement": "Your pressure response is to absorb load — what gets put on you stays put. TRUE: I take weight. I don't shed responsibilities. FALSE: I refuse loads that aren't mine. I won't be the bedrock by default.",
    },
    "cha_chuan_jin": {
        "english": "Hairpin Metal",
        "element": "Metal",
        "visibility_class": "compound",
        "strength_class": "enduring",
        "visibility_statement": "Your value shows up close — refined, personal, often unnoticed at a distance. TRUE: People who get close see the craft. Strangers miss me. FALSE: I'm obvious from far. The fine detail isn't the main thing.",
        "strength_statement": "Your pressure response is refined — you've been worked into your shape, and you hold it under tension. TRUE: I've been honed into who I am. I don't slip back. FALSE: I'm still in process. The shape isn't fixed yet.",
    },
    "sang_zhe_mu": {
        "english": "Mulberry Wood",
        "element": "Wood",
        "visibility_class": "visible",
        "strength_class": "adaptive",
        "visibility_statement": "Your value is in what you produce — practical, repeatable, supports other things to thrive. TRUE: I make what people need. The output is the point. FALSE: I do unique work, not output work. The product isn't the value.",
        "strength_statement": "Your pressure response is practical adaptation — you pivot to what works. TRUE: I adjust to demand. I don't get attached to one mode. FALSE: I do my work my way. The market doesn't decide what I make.",
    },
    "da_xi_shui": {
        "english": "Great Stream Water",
        "element": "Water",
        "visibility_class": "visible",
        "strength_class": "adaptive",
        "visibility_statement": "Your force is obvious — people see the current and either ride or step back. TRUE: I move with momentum people can't ignore. FALSE: My power is quieter than my chart says. I don't push that hard.",
        "strength_statement": "Your pressure response is to push through — direct force, no rerouting. TRUE: I overpower obstacles. I don't go around. FALSE: I'd rather flow around than smash through.",
    },
    "sha_zhong_tu": {
        "english": "Sand and Earth",
        "element": "Earth",
        "visibility_class": "mixed",
        "strength_class": "adaptive",
        "visibility_statement": "Your ground shifts — what you stand on isn't always stable. TRUE: My footing changes a lot. I've learned to move with it. FALSE: I have firm ground. The shifting isn't where I am.",
        "strength_statement": "Your pressure response is uncertainty — you don't always know what you'll do under stress. TRUE: I surprise myself in crises. Different versions of me show up. FALSE: I know who I am under pressure. No surprises.",
    },
    "tian_shang_huo": {
        "english": "Heavenly Fire",
        "element": "Fire",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "You operate at the highest visibility scale — when you're on, everyone sees you. TRUE: I'm meant to be at the center. Smaller stages don't fit. FALSE: I prefer not being the center. The supreme scale tires me out.",
        "strength_statement": "Your pressure response is overwhelming — your output dwarfs the obstacle. TRUE: I bring more than the situation requires. Force is on my side. FALSE: I match the situation. I don't go nuclear.",
    },
    "shi_liu_mu": {
        "english": "Pomegranate Wood",
        "element": "Wood",
        "visibility_class": "visible",
        "strength_class": "enduring",
        "visibility_statement": "Your output is visible and abundant — what you produce is the headline. TRUE: My fruit speaks for me. People see the abundance. FALSE: I'm in a fallow period. The abundance isn't where I am now.",
        "strength_statement": "Your pressure response is to keep producing — you fruit even in tough seasons. TRUE: I keep making things even when conditions are bad. FALSE: I need the right conditions. Forced production doesn't work for me.",
    },
    "da_hai_shui": {
        "english": "Great Sea Water",
        "element": "Water",
        "visibility_class": "mixed",
        "strength_class": "enduring",
        "visibility_statement": "Your depth is unfathomable — people see the surface and don't know the volume. TRUE: There's much more to me than people see. FALSE: What people see is most of what I am. I'm not hiding depth.",
        "strength_statement": "Your pressure response is to absorb without showing — the ocean doesn't care about a storm. TRUE: I take what comes without losing my shape. FALSE: I get rocked. Pressure does mark me visibly.",
    },
}


def visibility_impact_text(vis_class: str) -> str:
    """Map visibility_class → LLM-facing impact direction."""
    if vis_class == "compound":
        return "interpret toward long compound arcs, late-blooming wins, hidden mastery"
    if vis_class == "visible":
        return "interpret toward public-facing outcomes, recognition, visible milestones"
    return "interpret across both visible and hidden phases — both can be active"


def strength_impact_text(str_class: str) -> str:
    """Map strength_class → LLM-facing impact direction."""
    if str_class == "enduring":
        return "predict long single arcs with deep recovery periods, slow rebuilds, single dominant mode"
    if str_class == "adaptive":
        return "predict pivots, resets, new beginnings after setbacks, multiple modes"
    return "predict alternating modes — both endurance and adaptive cycles activate"
