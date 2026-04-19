"""
Starlogic — Star × Palace × Age interpretations
14 stars × 12 palaces × 5 age brackets (Child 0-12, Teen 13-19, Adult 20-39, Middle 40-59, Senior 60+)
Missing combos are intentionally omitted (e.g. Children palace for a child age).
"""

STAR_PALACE_AGE_EFFECTS = {

# ═══════════════════════════════════════════════════════════
# ZI WEI — Purple Star Emperor (EARTH) — supreme authority, sovereignty
# ═══════════════════════════════════════════════════════════
"zi_wei": {
    "Life": {
        "Child":  "recognized as natural leader by adults; receives attention and expectations beyond peers",
        "Teen":   "holds significant role in school or community; peers defer to them naturally",
        "Adult":  "promoted to authority position; recognized publicly as leader in their field",
        "Middle": "reaches peak authority — CEO, director, head of institution; commands full professional weight",
        "Senior": "transitions into elder statesman role; legacy and reputation solidify",
    },
    "Siblings": {
        "Child":  "eldest-child dynamic even if not oldest; takes charge of sibling group",
        "Teen":   "dominant figure in peer group; sets social agenda for friends",
        "Adult":  "leads business or creative team of peers; commands respect among equals",
        "Middle": "senior among professional peers; becomes the one others consult",
        "Senior": "elder statesman of old peer network",
    },
    "Spouse": {
        "Teen":   "first romantic partner is high-status, popular, or from prominent family",
        "Adult":  "marriage to someone with public standing or power; union elevates social position",
        "Middle": "partnership becomes publicly recognized unit; couple seen as established power couple",
        "Senior": "long marriage seen as exemplary; spouse achieves recognized standing",
    },
    "Children": {
        "Adult":  "child born with strong presence — early signs of leadership or performance ability",
        "Middle": "child reaches notable achievement (admission to top program, public recognition, athletic/artistic prominence)",
        "Senior": "grandchild shows leadership traits; child reaches professional peak",
    },
    "Wealth": {
        "Child":  "born into family of notable means or status; financial security assumed",
        "Teen":   "first significant earning or scholarship; financial recognition for achievement",
        "Adult":  "major income milestone reached; salary crosses significant threshold; equity position granted",
        "Middle": "net worth reaches peak level; controls substantial assets; financial sovereignty achieved",
        "Senior": "wealth preservation and legacy planning; estate structure formalized",
    },
    "Health": {
        "Child":  "strong constitution; recovers quickly from illness; robust physical presence",
        "Teen":   "athletic prominence or physical confidence; strong recovery from any setbacks",
        "Adult":  "health holds under heavy demands; pride may delay seeking help for early symptoms",
        "Middle": "constitution remains strong but ego resists medical advice; hypertension risk from authority stress",
        "Senior": "longevity likely; resistance to being a patient may complicate care",
    },
    "Travel": {
        "Child":  "family travels with prominence — relocated for parent's high-status role",
        "Teen":   "significant trip as representative of school or team; travel with purpose",
        "Adult":  "business travel for leadership purposes; relocates to more prestigious city",
        "Middle": "international role requiring travel; establishes residence in major global city",
        "Senior": "final major relocation to landmark location; travel as elder statesman",
    },
    "Friends": {
        "Child":  "befriends children of prominent families; social circle has status weight",
        "Teen":   "moves in influential circles; connections with teachers, coaches, mentors",
        "Adult":  "professional network includes powerful people; key allies are high-status",
        "Middle": "network is a genuine asset — includes executives, officials, established figures",
        "Senior": "connected to elder power networks; advisory circles",
    },
    "Career": {
        "Teen":   "first job or role carries unusual responsibility; recognized early as leadership material",
        "Adult":  "promoted to director/VP/management; authority granted formally",
        "Middle": "C-suite, partnership, or equivalent — top of field professionally",
        "Senior": "board positions, chairman role, emeritus status; final authority phase",
    },
    "Property": {
        "Child":  "family home is prominent — larger, better-located, or historically significant",
        "Teen":   "family upgrades residence substantially; moves to better neighborhood",
        "Adult":  "buys landmark property — notable home, commanding location, or multiple properties",
        "Middle": "property portfolio reaches peak; estate-level holdings",
        "Senior": "final estate consolidation; legacy property decisions",
    },
    "Fortune": {
        "Child":  "fated event establishes child's trajectory — scholarship, discovery of talent, adoption into opportunity",
        "Teen":   "destiny-level opening — scholarship to top school, discovery by mentor, competitive selection",
        "Adult":  "life-redirecting opportunity — promotion, offer, or appointment that changes course permanently",
        "Middle": "legacy-defining event; the year their life's work becomes publicly recognized",
        "Senior": "ceremonial recognition of life's work; final fate-level acknowledgment",
    },
    "Parents": {
        "Child":  "parent holds public standing, authority, or prominence; strong paternal archetype",
        "Teen":   "parent reaches career peak; family prestige grows",
        "Adult":  "parent recognized in later career; inheritance of social capital",
        "Middle": "parent passes authority to adult child; role reversal of leadership",
        "Senior": "parent's legacy formalized through inheritance or remembrance",
    },
},

# ═══════════════════════════════════════════════════════════
# TIAN JI — Heavenly Mechanism (WOOD) — intelligence, strategy
# ═══════════════════════════════════════════════════════════
"tian_ji": {
    "Life": {
        "Child":  "curious, observant, asks unusual questions; shows early aptitude for puzzles or systems",
        "Teen":   "academic recognition; strategic thinker among peers; analytical approach stands out",
        "Adult":  "positioned in role requiring analysis, strategy, or planning; advisor dynamic emerges",
        "Middle": "strategic architect of projects; known as the person who figures things out",
        "Senior": "sought for counsel and wisdom; planning mind remains sharp",
    },
    "Siblings": {
        "Child":  "sibling/peer intellectual competition; compared academically",
        "Teen":   "study groups or chess clubs; peer network built around intellectual activity",
        "Adult":  "business partner or collaborator is a strategist; sibling achieves academic/professional recognition",
        "Middle": "consulting relationships with peers; sibling becomes advisor or expert in their domain",
        "Senior": "old peer network reconvenes around shared expertise or knowledge",
    },
    "Spouse": {
        "Teen":   "first romantic partner is intellectual match; academic or strategic connection",
        "Adult":  "marries someone in analytical field (academic, engineer, consultant, analyst, doctor)",
        "Middle": "partnership operates as strategic alliance; shared planning defines marriage",
        "Senior": "long intellectual companionship; partnership remains mentally active",
    },
    "Children": {
        "Adult":  "child shows early analytical or verbal intelligence; parenting style is explanatory and strategic",
        "Middle": "child selected for advanced academic track; intellectual competition with other families",
        "Senior": "grandchildren show academic promise; parent becomes family strategist",
    },
    "Wealth": {
        "Child":  "family money comes through expertise (professional parents) or calculated moves",
        "Teen":   "first earning through intellectual work — tutoring, programming, research, strategic trades",
        "Adult":  "income through consulting, advisory, analysis, or calculated investments",
        "Middle": "wealth grows through strategic management of assets rather than active earning",
        "Senior": "wealth preserved through careful planning; estate organized strategically",
    },
    "Health": {
        "Child":  "sensitive nervous system; overthinks, worries; stress manifests as stomach or sleep issues",
        "Teen":   "anxiety from academic pressure; insomnia, overthinking during exams",
        "Adult":  "stress-related conditions from mental load; neck/back tension, sleep disruption",
        "Middle": "nervous system strain; potential for anxiety disorders, high cortisol, chronic tension",
        "Senior": "mental sharpness remains; physical complaints tied to nervous system rather than organs",
    },
    "Travel": {
        "Child":  "family relocates for educational opportunity (parent's research, better schools)",
        "Teen":   "study abroad, academic exchange, intellectually-motivated trip",
        "Adult":  "relocates for strategic career move; calculated geographic change",
        "Middle": "moves to intellectual/financial hub for career optimization",
        "Senior": "final relocation decision made analytically — cost, care, proximity to family factored",
    },
    "Friends": {
        "Child":  "forms small circle of smart friends; intellectual cliques over social popularity",
        "Teen":   "study group, debate team, academic peers become network",
        "Adult":  "professional advisory relationships; network of experts and strategists",
        "Middle": "trusted council of advisors; small circle of deep expertise",
        "Senior": "remaining friendships are the intellectually substantive ones",
    },
    "Career": {
        "Teen":   "first work shows analytical inclination — tech, research, planning roles",
        "Adult":  "consultant, strategist, analyst, advisor, academic, engineer — role requiring figuring things out",
        "Middle": "chief strategist, director of strategy, senior advisor, professor, domain expert",
        "Senior": "advisory board, emeritus, consulting in retirement, mentorship role",
    },
    "Property": {
        "Child":  "family home in university town or near intellectual hubs",
        "Teen":   "moves for parent's academic or strategic career move",
        "Adult":  "buys property strategically — location chosen for investment appreciation, not just living",
        "Middle": "real estate decisions driven by careful analysis; multiple properties as strategic holdings",
        "Senior": "downsizes strategically; property decisions run through careful planning",
    },
    "Fortune": {
        "Child":  "lucky placement in school, program, or opportunity through strategic parent planning",
        "Teen":   "scholarship, admission, or selection earned through calculated effort",
        "Adult":  "opportunity arrives through network and careful positioning; not random luck",
        "Middle": "strategic bet pays off; years of planning yield unexpected gain",
        "Senior": "foresight from decades ago proves valuable; planning pays forward",
    },
    "Parents": {
        "Child":  "parent is educator, analyst, researcher, or strategist; household is intellectually active",
        "Teen":   "parent's expertise shapes teen's direction; academic pressure from parents",
        "Adult":  "parent becomes consultant, advisor; relationship becomes more intellectually equal",
        "Middle": "parent's analytical mind remains sharp; strategic family discussions",
        "Senior": "parent's wisdom continues to inform; planning decisions made together",
    },
},

# ═══════════════════════════════════════════════════════════
# TAI YANG — Sun (FIRE) — male authority, outward radiation, public service
# ═══════════════════════════════════════════════════════════
"tai_yang": {
    "Life": {
        "Child":  "bright, outgoing, generous to friends; visible in school settings",
        "Teen":   "popular, involved in visible activities (student government, sports, performance)",
        "Adult":  "public-facing role; recognized in wider community; generosity that sometimes exceeds means",
        "Middle": "publicly known in field; significant reputation; energy starts depleting from over-giving",
        "Senior": "respected elder with known public legacy; health costs from decades of outward focus",
    },
    "Siblings": {
        "Child":  "protective older-brother dynamic with siblings/cousins; generous with peers",
        "Teen":   "leader of friend group; hosts, gathers, includes everyone; social hub role",
        "Adult":  "mentor to younger siblings or colleagues; professional generosity visible",
        "Middle": "mentor figure in professional community; gives more than receives",
        "Senior": "respected elder in extended family; generosity acknowledged across generations",
    },
    "Spouse": {
        "Teen":   "first relationship with someone generous but possibly over-extending themselves",
        "Adult":  "marries generous, outward-focused person; partner may sacrifice too much for others",
        "Middle": "partnership has public-facing element; one or both known in community; generosity a theme",
        "Senior": "long partnership built on giving; spouse's generosity has shaped life together",
    },
    "Children": {
        "Adult":  "child born into visibility (social, public, recognized family); proud public presentation",
        "Middle": "child achieves public recognition — award, media, competition win",
        "Senior": "child/grandchild becomes publicly known; family name carried visibly",
    },
    "Wealth": {
        "Child":  "family money from visible/public work (medicine, teaching, public service, performance)",
        "Teen":   "first earning through visible work (tutoring, performance, service); money earned is often shared",
        "Adult":  "income through public-facing career; money flows in and out generously; giving is significant line item",
        "Middle": "wealth tied to reputation and public role; substantial charitable giving",
        "Senior": "wealth partly depleted through lifelong generosity; legacy in people helped rather than accumulated",
    },
    "Health": {
        "Child":  "strong at first but prone to heart/eye issues; energy spent on social activity",
        "Teen":   "eye strain from screens and study; heart symptoms from overexertion in sports",
        "Adult":  "blood pressure, heart concerns, eye issues; burnout from giving too much",
        "Middle": "cardiovascular issues emerge; vision requires correction; energy reserves lower from decades of output",
        "Senior": "heart conditions, cataracts, circulation issues; body shows wear from outward-focused life",
    },
    "Travel": {
        "Child":  "family travels for visible reasons (performances, competitions, religious/service trips)",
        "Teen":   "trips that involve representing — team, school, country; visible travel",
        "Adult":  "business travel for public-facing role; speaking, performing, teaching elsewhere",
        "Middle": "travels as recognized authority; speaking circuits, conference keynotes, mission work",
        "Senior": "ceremonial travel; return visits as respected elder",
    },
    "Friends": {
        "Child":  "many friends, open with all; generous with time and attention",
        "Teen":   "wide social circle; known across cliques; generous with friends to own cost",
        "Adult":  "large professional network; known broadly; gives more than gets from connections",
        "Middle": "respected across multiple communities; benefactor dynamic common",
        "Senior": "wide network of people helped over decades; many show up in later years",
    },
    "Career": {
        "Teen":   "first work in public-facing role — retail, service, tutoring, performance, camp counseling",
        "Adult":  "teaching, medicine, public service, media, ministry, performance — outward radiating work",
        "Middle": "senior role in public-facing field; department head, lead physician, principal, recognized performer",
        "Senior": "emeritus, honored retirement, continued service in advisory or mentorship capacity",
    },
    "Property": {
        "Child":  "family home is central gathering place; open-door household",
        "Teen":   "family home known in community; location prominent",
        "Adult":  "buys home that faces outward — hosts gatherings, entertaining space, visible location",
        "Middle": "property becomes community hub; home used for events, gatherings, public-facing purposes",
        "Senior": "home remains gathering place; passing to next generation as anchor point",
    },
    "Fortune": {
        "Child":  "public recognition early — award, feature, notable achievement in school",
        "Teen":   "visible opportunity — scholarship announced publicly, selection for prominent role",
        "Adult":  "luck arrives through visibility; being known creates the opening",
        "Middle": "reputation itself becomes the asset; opportunities come unsolicited",
        "Senior": "lifetime of visible service returns as support, recognition, or blessing",
    },
    "Parents": {
        "Child":  "strong father figure or father-surrogate; public/professional father",
        "Teen":   "father's career or reputation shapes teen's context; paternal pressure significant",
        "Adult":  "father's career peaks or transitions; relationship with father significant this year",
        "Middle": "father ages, role reverses; child becomes parent's public representative",
        "Senior": "father passes or memorial moment; paternal legacy becomes conscious",
    },
},

# ═══════════════════════════════════════════════════════════
# WU QU — Military Wealth (METAL) — disciplined earning, martial money
# ═══════════════════════════════════════════════════════════
"wu_qu": {
    "Life": {
        "Child":  "disciplined, serious kid; takes rules and structure seriously; tough exterior",
        "Teen":   "financially driven early — saves money, works part-time, tracks earnings carefully",
        "Adult":  "professionally disciplined; recognized for work ethic and financial competence",
        "Middle": "defined by financial discipline and professional rigor; tough reputation",
        "Senior": "financially prepared for later life; disciplined lifestyle continues",
    },
    "Siblings": {
        "Child":  "competitive with siblings/peers about money, grades, achievement",
        "Teen":   "peer competition around jobs, savings, college admissions — measured and tracked",
        "Adult":  "business partnerships built on clear financial terms; siblings compete professionally",
        "Middle": "professional peers compared on financial success; sibling financial conflicts possible",
        "Senior": "inheritance and estate discussions with siblings; financial legacy conversations",
    },
    "Spouse": {
        "Teen":   "first serious partner is practical, goal-oriented, financially minded",
        "Adult":  "marries financially practical person; prenup or explicit money discussions; finances structured",
        "Middle": "partnership has rigorous financial structure; money is a defining theme of marriage",
        "Senior": "long partnership with shared financial discipline; estate planning together",
    },
    "Children": {
        "Adult":  "child raised with structure and financial discipline from early age",
        "Middle": "teaching children explicit financial habits; discipline-focused parenting",
        "Senior": "adult children follow financial discipline modeled by parent; inheritance structured",
    },
    "Wealth": {
        "Child":  "family lives within means, saves carefully, explicit about money with children",
        "Teen":   "first earnings tracked carefully; saving becomes habitual; financial responsibility early",
        "Adult":  "income grows through disciplined earning, not speculation; savings rate high",
        "Middle": "peak earning years with strong financial discipline; significant accumulation",
        "Senior": "wealth preserved through lifelong discipline; financial security solid",
    },
    "Health": {
        "Child":  "respiratory conditions — asthma, frequent colds, sinus issues",
        "Teen":   "breathing issues from sports or environment; athletic but susceptible to injury",
        "Adult":  "respiratory or skeletal issues; strong but susceptible to sudden breaks rather than gradual decline",
        "Middle": "lung conditions, joint issues, dental problems; metal-element vulnerabilities",
        "Senior": "respiratory conditions may dominate later health (COPD, chronic bronchitis, lung cancer risk)",
    },
    "Travel": {
        "Child":  "family moves for parent's structured job — military base, corporate relocation, financial role",
        "Teen":   "trips are purposeful and budgeted; study abroad chosen for economic benefit",
        "Adult":  "business travel with clear financial purpose; relocation for better earning",
        "Middle": "moves for financial optimization — lower taxes, better markets, better financial opportunity",
        "Senior": "final moves made on financial grounds — cost of living, estate considerations",
    },
    "Friends": {
        "Child":  "small circle of reliable friends; loyalty over breadth",
        "Teen":   "competitive peer group around achievement; earned friendships rather than easy ones",
        "Adult":  "professional network of competent, disciplined people; friendships provide business value",
        "Middle": "small circle of trusted, high-achieving peers; no room for casual connections",
        "Senior": "lifelong loyal friends — disciplined in maintaining relationships",
    },
    "Career": {
        "Teen":   "first job in structured environment — military consideration, finance, construction, security",
        "Adult":  "finance, military, law enforcement, engineering, operations — structured disciplined work",
        "Middle": "CFO, director of operations, military officer rank, senior engineer — disciplined authority",
        "Senior": "respected retirement from disciplined field; consulting in domain of expertise",
    },
    "Property": {
        "Child":  "family home is solid, well-maintained, not showy; built to last",
        "Teen":   "family home paid off or actively being paid down; financial focus on housing",
        "Adult":  "buys property as financial asset, not lifestyle statement; calculated purchase",
        "Middle": "property portfolio focused on cash flow and appreciation; rentals common",
        "Senior": "property remains financial cornerstone; mortgage paid off; estate-ready",
    },
    "Fortune": {
        "Child":  "fortune comes through family's financial discipline creating opportunity",
        "Teen":   "scholarship, internship, or opportunity earned through hard work and precision",
        "Adult":  "gains come through disciplined action, not luck; financial windfalls earned",
        "Middle": "fortune is the compound result of decades of discipline",
        "Senior": "later years financially secure through disciplined preparation",
    },
    "Parents": {
        "Child":  "parents financially strict; household money rules explicit; military or disciplined household",
        "Teen":   "parental pressure around financial responsibility; expected to work or contribute",
        "Adult":  "parents continue to model financial discipline; inheritance or gifts structured",
        "Middle": "parent's financial legacy transfers; inheritance handled with discipline",
        "Senior": "parent's disciplined estate structure preserves wealth across generations",
    },
},

# ═══════════════════════════════════════════════════════════
# TIAN TONG — Heavenly Unity (WATER) — comfort, harmony, ease
# ═══════════════════════════════════════════════════════════
"tian_tong": {
    "Life": {
        "Child":  "easygoing, pleasant child; gets along with everyone; youthful appearance maintained",
        "Teen":   "popular without trying; avoids drama; comfort-seeking in choices",
        "Adult":  "makes life choices that prioritize comfort and enjoyment over ambition",
        "Middle": "comfortable life established; work-life balance prioritized; lower-stress path chosen",
        "Senior": "youthful vitality in later years; age gracefully without major decline",
    },
    "Siblings": {
        "Child":  "harmonious sibling relationships; little conflict; mutual support",
        "Teen":   "easy peer friendships; low-drama social life",
        "Adult":  "non-competitive peer relationships; collaborative rather than competitive dynamics",
        "Middle": "peer group maintained through shared enjoyment rather than obligation",
        "Senior": "lifelong friendships remain easy and pleasant into later years",
    },
    "Spouse": {
        "Teen":   "first relationship comfortable and low-drama; compatible without intensity",
        "Adult":  "marries for harmony and compatibility rather than passion; stable easy partnership",
        "Middle": "marriage is genuinely comfortable companion partnership; conflict avoidance is default",
        "Senior": "long marriage defined by companionship and mutual comfort",
    },
    "Children": {
        "Adult":  "easygoing child, playful parenting style, low-conflict household",
        "Middle": "children raised with emphasis on happiness and balance rather than achievement pressure",
        "Senior": "grandchildren bring joy; relationship with adult children remains harmonious",
    },
    "Wealth": {
        "Child":  "family comfortable but not driven to accumulate; lives well without ostentation",
        "Teen":   "money comes for comfort and enjoyment rather than achievement signaling",
        "Adult":  "passive income streams prioritized over active hustling; comfort-focused earning",
        "Middle": "wealth sufficient for comfortable life; less drive to maximize accumulation",
        "Senior": "financially comfortable for later years; enough rather than excess",
    },
    "Health": {
        "Child":  "generally healthy, quick recovery; susceptible to overindulgence in food/sweets",
        "Teen":   "weight gain from comfort eating; susceptibility to lazy health habits",
        "Adult":  "metabolic issues from comfort-seeking lifestyle — weight, diabetes risk, sedentary concerns",
        "Middle": "health issues from accumulated comfort — blood sugar, weight, fatty liver, inactivity",
        "Senior": "remains comfortable but decline through lack of challenge; gentle age-related conditions",
    },
    "Travel": {
        "Child":  "family vacations to enjoyable destinations; travel is for pleasure not adventure",
        "Teen":   "trips chosen for comfort and fun; resort or beach vacations",
        "Adult":  "travel is leisure-focused; comfortable accommodations prioritized",
        "Middle": "travel as reward for work; resort lifestyle, cruises, comfortable tourism",
        "Senior": "gentle travel continues; comfortable destinations chosen for later years",
    },
    "Friends": {
        "Child":  "liked by everyone; easy friendships across groups",
        "Teen":   "pleasant social life; no enemies; wide but shallow connections",
        "Adult":  "comfortable social network focused on shared enjoyment rather than professional advantage",
        "Middle": "social circle built around leisure — golf partners, dinner friends, hobby community",
        "Senior": "leisure-based friendships remain vibrant into retirement",
    },
    "Career": {
        "Teen":   "first job is low-stress — hospitality, service, entertainment, easy retail",
        "Adult":  "chooses career that balances work and life; avoids high-stress paths",
        "Middle": "settles into comfortable professional role; declines promotions that would disrupt balance",
        "Senior": "smooth retirement transition; comfortable winding down",
    },
    "Property": {
        "Child":  "family home comfortable and pleasant; not grand but welcoming",
        "Teen":   "family home remains stable throughout teen years; no major moves",
        "Adult":  "buys home for comfort rather than investment — livability over appreciation",
        "Middle": "home improvements focus on enjoyment — pool, garden, entertainment space",
        "Senior": "ages in place in comfortable home; resists major moves",
    },
    "Fortune": {
        "Child":  "lucky breaks come without effort; gentle good fortune",
        "Teen":   "things work out easily; opportunities arrive through comfort and likability",
        "Adult":  "luck flows through relationships and enjoyment rather than striving",
        "Middle": "comfortable life itself is the fortune; stability is the blessing",
        "Senior": "gentle fortune in later years; comfortable retirement realized",
    },
    "Parents": {
        "Child":  "gentle, non-demanding parents; pleasant household; indulgent rather than strict",
        "Teen":   "low-conflict relationship with parents; comfortable home during adolescence",
        "Adult":  "parents remain supportive without pressure; easy adult relationship",
        "Middle": "parents age comfortably; caretaking is gentle rather than crisis-driven",
        "Senior": "parents passed peacefully or still present comfortably; gentle end-of-life trajectory",
    },
},

# ═══════════════════════════════════════════════════════════
# LIAN ZHEN — Chastity (FIRE) — intensity, complexity, obsessive focus
# ═══════════════════════════════════════════════════════════
"lian_zhen": {
    "Life": {
        "Child":  "intense, guarded child; strong feelings not always expressed; complex inner world",
        "Teen":   "intense adolescence — strong passions, complex identity, possible rebellion",
        "Adult":  "passionate about work or cause; complex inner life; charming exterior masks intensity",
        "Middle": "defined by obsessive focus on craft or mission; intense at peak influence",
        "Senior": "intensity mellows but complexity remains; strong personality persists",
    },
    "Siblings": {
        "Child":  "complicated sibling dynamic — intense loyalty or intense rivalry",
        "Teen":   "peer relationships charged with intensity; jealousy, loyalty, betrayal themes",
        "Adult":  "intense partnerships with peers — creative collaboration or competitive feud",
        "Middle": "complex professional rivalries; loyal collaborators or bitter competitors",
        "Senior": "old peer relationships still carry emotional weight; unresolved tensions remain",
    },
    "Spouse": {
        "Teen":   "first relationship intense, possessive, dramatic; not casual",
        "Adult":  "marriage is passionate and complicated; jealousy, devotion, complexity mixed",
        "Middle": "partnership has history of intensity; loyal but complex; affairs or near-affairs possible",
        "Senior": "long passionate marriage with complicated history; deep bond through complexity",
    },
    "Children": {
        "Adult":  "intense parenting style; complex feelings about parenthood; child becomes focus of intensity",
        "Middle": "complex relationship with teen children; intensity creates conflict or devotion",
        "Senior": "deep complex bond with adult children; family intensity carries forward",
    },
    "Wealth": {
        "Child":  "family wealth has complicated backstory — earned, lost, recovered, or contested",
        "Teen":   "first money comes through intense effort or unusual means",
        "Adult":  "income through passion work that is also complex — entertainment, law, politics, legal practice",
        "Middle": "wealth complicated by lifestyle, obligations, or passionate spending",
        "Senior": "financial picture in later years reflects intense life choices",
    },
    "Health": {
        "Child":  "intense emotional episodes affect body; sensitive to household tension",
        "Teen":   "emotional intensity manifests as skin conditions, heart racing, sleep issues",
        "Adult":  "heart fire — cardiovascular stress, sexual health issues, inflammation",
        "Middle": "heart conditions, STI risks from intensity, autoimmune conditions",
        "Senior": "cardiac issues, long-term effects of intense lifestyle manifest in body",
    },
    "Travel": {
        "Child":  "family trips have complicated backstory — trips for legal/medical/family intensity reasons",
        "Teen":   "intense travel experience that leaves lasting impression; transformative trip",
        "Adult":  "travel tied to passion project or complex situation; intense journeys",
        "Middle": "travel for complex reasons — affair, legal matter, passionate pursuit",
        "Senior": "return trips to places of intensity; memorial or reconciliation travel",
    },
    "Friends": {
        "Child":  "deep, intense friendships; small circle with strong loyalty bonds",
        "Teen":   "friend group with drama and loyalty themes; intense peer attachments",
        "Adult":  "close friends are intense loyal allies; wide acquaintance but few true intimates",
        "Middle": "long-term intense loyalties; feuds with old friends possible",
        "Senior": "remaining close friends are the ones who survived the intensity of decades",
    },
    "Career": {
        "Teen":   "first work in intense environment — entertainment, performance, emergency services",
        "Adult":  "law, politics, entertainment, performance, activism — passionate complex work",
        "Middle": "senior role in intense field; known for passionate commitment",
        "Senior": "reputation for intensity remains; advisory or ceremonial role in passion field",
    },
    "Property": {
        "Child":  "family home has complicated history — renovation, inherited, contested, restored",
        "Teen":   "family home is complex — renovation during teen years, emotional relocations",
        "Adult":  "buys property with complications — fixer-upper, property with history, contested purchase",
        "Middle": "renovation as passion project; property becomes expression of intensity",
        "Senior": "home holds decades of complex memory; relationship with property is emotional",
    },
    "Fortune": {
        "Child":  "family crisis that intensifies child's early experience; passionate formative events",
        "Teen":   "transformative event with romantic/intense quality; first great loss or great passion",
        "Adult":  "luck through intensity — passion project succeeds, obsessive work pays off",
        "Middle": "life's passion brings recognition or crisis; intensity as double-edged fortune",
        "Senior": "later-life fortune reflects intensity of earlier commitments",
    },
    "Parents": {
        "Child":  "intense parental relationship — passionate love or complex dynamic; strong personalities",
        "Teen":   "parent's intensity creates teen conflict or deep bond; family drama significant",
        "Adult":  "complex adult relationship with parent; intensity continues",
        "Middle": "aging parent's intensity continues to shape family; complex caregiving",
        "Senior": "parent's death carries intense processing; complicated grief or deep peace",
    },
},

# ═══════════════════════════════════════════════════════════
# TIAN FU — Celestial Vault (EARTH) — stored wealth, accumulation, security
# ═══════════════════════════════════════════════════════════
"tian_fu": {
    "Life": {
        "Child":  "stable, reliable child; not flashy but trusted; sense of groundedness early",
        "Teen":   "reliable teen; parents and teachers trust them; conservative choices",
        "Adult":  "professionally stable; builds reputation for reliability and wealth-attracting presence",
        "Middle": "financially established; peak accumulation years; trusted authority on stability",
        "Senior": "wealth and stability solidified; comfortable elder with resources",
    },
    "Siblings": {
        "Child":  "cooperative sibling relationships; shared family wealth stability",
        "Teen":   "peer group stable and prosperous; financial cooperation among friends",
        "Adult":  "business partnerships with prosperous peers; shared wealth building",
        "Middle": "financial network of peers; established in wealthy peer group",
        "Senior": "remaining peers are long-term wealth partners; estate-level peer support",
    },
    "Spouse": {
        "Teen":   "first relationship with someone stable, reliable, possibly from financially established family",
        "Adult":  "marries financially stable person; marriage includes significant financial security",
        "Middle": "partnership is genuinely a financial vault — pooled assets build substantially",
        "Senior": "long stable partnership with accumulated shared wealth",
    },
    "Children": {
        "Adult":  "child born into financial stability; abundance provided for",
        "Middle": "investing heavily in children's future — education funds, property, legacy planning",
        "Senior": "grandchildren beneficiaries of generational wealth; legacy planning explicit",
    },
    "Wealth": {
        "Child":  "family wealth stable and accumulated across generations; financial abundance assumed",
        "Teen":   "first income saved and invested rather than spent; early wealth habits",
        "Adult":  "peak accumulation years — investments grow, assets compound, net worth crosses thresholds",
        "Middle": "vault opens — major financial milestone, company equity vests, property appreciates significantly",
        "Senior": "wealth preserved and structured for multi-generational transfer; estate substantial",
    },
    "Health": {
        "Child":  "stable health; robust constitution; slight overweight possible from good eating",
        "Teen":   "generally healthy, stable body; weight management is theme",
        "Adult":  "stable health with digestive focus; accumulation shows up in body too (weight, cholesterol)",
        "Middle": "metabolic issues from accumulation — diabetes risk, cholesterol, hypertension",
        "Senior": "stable aging with digestive/metabolic concerns; generally healthy longevity",
    },
    "Travel": {
        "Child":  "family travels comfortably; stable family vacations to nice destinations",
        "Teen":   "comfortable travel; not extreme adventure but solid memorable trips",
        "Adult":  "travels for business comfortably; relocates to more prosperous area",
        "Middle": "moves to prestigious or wealthier area; second home in desirable location",
        "Senior": "travel in later years remains comfortable; multiple residences possible",
    },
    "Friends": {
        "Child":  "friends come from stable families; network stable across childhood",
        "Teen":   "peer group remains consistent; friends from prosperous background",
        "Adult":  "network of financially established peers; friends bring genuine resources",
        "Middle": "connections open doors — introductions to money, opportunities, partnerships",
        "Senior": "old network remains valuable; resource-sharing peer group",
    },
    "Career": {
        "Teen":   "first work stable — bank teller, office work, family business, steady hours",
        "Adult":  "banking, finance, treasury, real estate, wealth management — resource management careers",
        "Middle": "senior finance role, wealth management, bank officer, investment manager, estate planner",
        "Senior": "comfortable retirement with continued financial oversight of portfolio",
    },
    "Property": {
        "Child":  "family owns home outright or with strong equity; property is foundational asset",
        "Teen":   "family upgrades or expands residence during teen years",
        "Adult":  "buys prime property; real estate as primary wealth vehicle",
        "Middle": "property portfolio peaks — multiple properties, valuable holdings, landmark residence",
        "Senior": "property wealth preserved; estate-level real estate decisions",
    },
    "Fortune": {
        "Child":  "born into or early encounter with accumulated blessing; stored family karma pays forward",
        "Teen":   "fortunate inheritance, scholarship, or opportunity with financial dimension",
        "Adult":  "fortune arrives as structural wealth — equity vesting, property appreciation, inheritance",
        "Middle": "decades of accumulation yield compound returns; wealth becomes self-sustaining",
        "Senior": "stored karma pays out as comfortable later years and meaningful legacy",
    },
    "Parents": {
        "Child":  "financially stable parents; household has accumulated resources; wealth values taught",
        "Teen":   "parents continue financial stability; teen benefits from family resources",
        "Adult":  "inheritance or significant parental financial support becomes factor",
        "Middle": "parents' estate planning explicit; significant inheritance or transfer",
        "Senior": "parents' wealth transferred; estate settled; financial legacy realized",
    },
},

# ═══════════════════════════════════════════════════════════
# TAI YIN — Moon (WATER) — feminine, internal, reflective, emotional
# ═══════════════════════════════════════════════════════════
"tai_yin": {
    "Life": {
        "Child":  "sensitive, intuitive child; reads emotional rooms; rich inner life; fragile temperament",
        "Teen":   "emotionally intense teen years; artistic expression; possible depression or anxiety",
        "Adult":  "emotionally attuned, intuitive professionally; artistic or caregiving orientation",
        "Middle": "emotional depth continues; possible emotional exhaustion from sensitivity",
        "Senior": "intuitive wisdom in later years; emotional patterns of lifetime integrate",
    },
    "Siblings": {
        "Child":  "emotionally bonded with siblings; sensitive to sibling's emotional states",
        "Teen":   "female friendships important; emotional peer attachments deep",
        "Adult":  "female allies and networks significant; sisters or sister-figures important",
        "Middle": "women's network remains a primary support system",
        "Senior": "women friends of decades remain most important connections",
    },
    "Spouse": {
        "Teen":   "first deep emotional relationship; sensitive partner",
        "Adult":  "marries emotionally deep person; partnership is emotionally rich and intimate",
        "Middle": "deep emotional intimacy with partner; possibly challenged by partner's moods or health",
        "Senior": "long emotionally rich marriage; deep bond of decades",
    },
    "Children": {
        "Adult":  "emotionally attuned parenting; daughter relationship particularly meaningful",
        "Middle": "nurturing adolescent child through emotional years; artistic or sensitive offspring",
        "Senior": "deep bond with adult children; grandchildren especially meaningful",
    },
    "Wealth": {
        "Child":  "family income from mother's work or traditionally feminine industries",
        "Teen":   "first money through sensitive work — tutoring young children, creative work, caregiving",
        "Adult":  "income through real estate, feminine industries (beauty, fashion, wellness, design, childcare)",
        "Middle": "wealth grows gradually through patient real estate or female-dominated industry",
        "Senior": "steady income from accumulated real estate; wealth built patiently",
    },
    "Health": {
        "Child":  "sensitive constitution; emotional states affect body; sleep issues from sensitivity",
        "Teen":   "hormonal sensitivity; menstrual issues for girls; emotional health concerns; sleep patterns",
        "Adult":  "hormonal issues, reproductive health concerns, sleep disorders; emotional-body connection strong",
        "Middle": "perimenopause/menopause issues for women; hormonal shifts; emotional-physical integration",
        "Senior": "sleep patterns remain theme; emotional health key to physical health",
    },
    "Travel": {
        "Child":  "family travel shaped by mother's preferences or needs; emotional trips",
        "Teen":   "emotional journey trips — grandparents, family reunions, meaningful return",
        "Adult":  "moves for emotional reasons — closer to family, leaving painful situation, following heart",
        "Middle": "relocation for emotional or caregiving reasons; following daughter, mother, or emotional pull",
        "Senior": "travel close to family; emotional returns to meaningful places",
    },
    "Friends": {
        "Child":  "deep emotional friendships with few close friends; tends to best-friend pairs",
        "Teen":   "intimate friendships with emotional depth; few but intense",
        "Adult":  "female-centered friendships; emotionally intimate peer group",
        "Middle": "deep female friendships remain crucial; emotional circle curated",
        "Senior": "oldest emotional bonds are the ones that matter",
    },
    "Career": {
        "Teen":   "first work involves care, creativity, or behind-scenes — nannying, art, design, library",
        "Adult":  "real estate, design, beauty industry, caregiving, night shift work, artistic careers",
        "Middle": "senior role in feminine or artistic field; mentor to younger women",
        "Senior": "artistic legacy, mentorship, or property management continues in retirement",
    },
    "Property": {
        "Child":  "family home beautiful or has distinctive character; mother's touch evident",
        "Teen":   "home is emotional anchor; aesthetic of house matters",
        "Adult":  "buys beautiful home; real estate as primary wealth vehicle; mother's influence on purchase",
        "Middle": "expands real estate holdings; beautiful properties curated carefully",
        "Senior": "beloved home remains anchor; passes to daughter or emotional heir",
    },
    "Fortune": {
        "Child":  "fortune through mother's blessing or female ancestor's influence",
        "Teen":   "emotional event that shapes destiny — a relationship, loss, or bonding experience",
        "Adult":  "luck arrives through patience and sensitivity; gradual good fortune",
        "Middle": "accumulated emotional intelligence becomes genuine asset; wisdom pays off",
        "Senior": "later-life fortune through patient accumulation and emotional wisdom",
    },
    "Parents": {
        "Child":  "strong mother-figure or female caregiver; maternal influence defining",
        "Teen":   "mother's emotional world shapes teen's understanding; maternal bond central",
        "Adult":  "adult relationship with mother remains primary family bond",
        "Middle": "caring for aging mother; role reversal; mother's final decades meaningful",
        "Senior": "mother's death significant turning point; matrilineal legacy conscious",
    },
},

# ═══════════════════════════════════════════════════════════
# TAN LANG — Greedy Wolf (WATER) — desire, charisma, appetite, magnetism
# ═══════════════════════════════════════════════════════════
"tan_lang": {
    "Life": {
        "Child":  "charismatic child; magnetic personality; many interests; restless",
        "Teen":   "sexually precocious; multi-talented; socially magnetic; tries many things",
        "Adult":  "charismatic professional; multiple income streams or interests; restless ambition",
        "Middle": "established charisma; still restless but more focused; managing multiple domains",
        "Senior": "magnetic elder; sexual vitality remains; many interests still active",
    },
    "Siblings": {
        "Child":  "socially competitive with peers; charisma measured against others",
        "Teen":   "peer popularity is theme; many friends across groups",
        "Adult":  "professionally charismatic peers; social dominance among colleagues",
        "Middle": "many professional connections; wide influential network",
        "Senior": "social magnetism persists into later life; many connections from across decades",
    },
    "Spouse": {
        "Teen":   "first relationship intense, sexually charged, magnetic; possible infidelity themes early",
        "Adult":  "passionate magnetic marriage; infidelity risk high on one side; sexual intensity",
        "Middle": "marriage has history of passion and complication; possible affair period",
        "Senior": "long marriage that survived intensity; or remarriage later in life",
    },
    "Children": {
        "Adult":  "talented children with many interests; creative and charismatic offspring",
        "Middle": "teenage children magnetic, popular; multiple interests shared with parent",
        "Senior": "adult children successful in creative or social fields",
    },
    "Wealth": {
        "Child":  "family money from charismatic work (sales, entertainment) or multiple streams",
        "Teen":   "first money through charm — sales, performance, influence; charismatic earning",
        "Adult":  "multiple income streams; sales commission, influence marketing, entertainment earnings",
        "Middle": "wealth from charisma-based career; peak earning through personal brand",
        "Senior": "wealth legacy from charisma-based career; continuing royalties or residuals",
    },
    "Health": {
        "Child":  "energetic child; appetite strong; possible excess in food, sugar, stimulation",
        "Teen":   "substance experimentation, sexual health, reproductive health concerns emerge",
        "Adult":  "liver issues from indulgence; reproductive or sexual health concerns",
        "Middle": "liver, reproductive, or addiction-related health issues; accumulated excess shows",
        "Senior": "liver disease, diabetes, reproductive cancers, effects of lifetime appetite",
    },
    "Travel": {
        "Child":  "family travels to exciting stimulating destinations; new experiences valued",
        "Teen":   "travel as exploration; study abroad, adventure trips, romantic international trips",
        "Adult":  "restless movement; frequent travel for work and pleasure; multiple locations",
        "Middle": "international circuit of homes or business; continuous movement",
        "Senior": "still traveling in later years; restless to the end",
    },
    "Friends": {
        "Child":  "wide friend group across cliques; charismatic child knows everyone",
        "Teen":   "extensive social network; popular but shallow connections; many acquaintances",
        "Adult":  "wide professional and social network; magnetic draw brings opportunities",
        "Middle": "extensive influential network; knows everyone in their industry/field",
        "Senior": "wide network persists; remains socially connected into later life",
    },
    "Career": {
        "Teen":   "first work in charismatic field — sales, performance, service, hospitality",
        "Adult":  "sales, marketing, entertainment, performance, hospitality, influence-based work",
        "Middle": "peak performance career; known for charisma in their field",
        "Senior": "continuing charismatic work in retirement; speaker circuits, consulting on charm",
    },
    "Property": {
        "Child":  "family moves frequently or has multiple residences; unsettled housing",
        "Teen":   "family home is social hub; parties, gatherings, multiple guests",
        "Adult":  "buys multiple properties or moves frequently; restless housing pattern",
        "Middle": "property portfolio in multiple locations; lifestyle real estate",
        "Senior": "multiple residences remain; final consolidation uncertain",
    },
    "Fortune": {
        "Child":  "lucky social positioning; charisma opens doors from early age",
        "Teen":   "opportunities arrive through magnetism — modeling, acting, being noticed",
        "Adult":  "luck follows charisma; appetite attracts opportunity; wide-net approach pays",
        "Middle": "years of cultivated charm yield compound opportunities; persona pays off",
        "Senior": "continued luck through social capital built over lifetime",
    },
    "Parents": {
        "Child":  "parents are charismatic, indulgent, possibly with strong appetites themselves",
        "Teen":   "parent's desires and appetites shape household; maybe party household",
        "Adult":  "complex adult relationship with charismatic parent; lessons learned from parent's appetite",
        "Middle": "aging parent's lifestyle choices catch up; caregiving affected by parent's history",
        "Senior": "parent's lifetime of appetite had consequences; memorial processes complex",
    },
},

# ═══════════════════════════════════════════════════════════
# JU MEN — Giant Gate (WATER) — speech, argument, criticism
# ═══════════════════════════════════════════════════════════
"ju_men": {
    "Life": {
        "Child":  "verbal, argumentative child; asks hard questions; challenges authority",
        "Teen":   "debate team energy; sharp tongue; good at arguing; may be bullied or be bully",
        "Adult":  "sharp communicator; known for critique or advocacy; verbally powerful",
        "Middle": "defined by ability to articulate or critique; writer, lawyer, teacher, analyst",
        "Senior": "sharp mind and voice continue; elder who still speaks truth",
    },
    "Siblings": {
        "Child":  "argued constantly with siblings; verbal competition",
        "Teen":   "debate-oriented peer group; verbal sparring with friends",
        "Adult":  "professional disagreements with peers; verbal clashes",
        "Middle": "ongoing professional rivalries expressed through argument",
        "Senior": "old verbal conflicts never fully resolved",
    },
    "Spouse": {
        "Teen":   "first relationship with verbal conflict; arguments a feature",
        "Adult":  "marriage characterized by verbal conflict; arguments are significant",
        "Middle": "partnership continues to have verbal conflict; disputes about values",
        "Senior": "long marriage with persistent verbal patterns; either resolved or ongoing",
    },
    "Children": {
        "Adult":  "argumentative or verbal child; communication is family focus",
        "Middle": "teen children challenge parent verbally; communication-focused family",
        "Senior": "adult children may have verbal conflicts with parent over values",
    },
    "Wealth": {
        "Child":  "family money from verbal work — law, teaching, writing, media",
        "Teen":   "first money through speaking/writing — tutoring, debate prizes, journalism, writing",
        "Adult":  "income through argument — law, consulting, analysis, broadcasting, teaching",
        "Middle": "wealth from accumulated verbal expertise and reputation",
        "Senior": "continuing income from speaking, writing, or advisory based on verbal reputation",
    },
    "Health": {
        "Child":  "throat issues — chronic sore throats, tonsil problems, voice issues",
        "Teen":   "throat, dental, stress-related stomach issues from verbal competition",
        "Adult":  "throat, mouth, digestive issues from verbal work; vocal cord issues for speakers",
        "Middle": "chronic throat/dental issues, GERD, digestive problems from verbal stress",
        "Senior": "voice and swallowing issues in later years; dental problems",
    },
    "Travel": {
        "Child":  "family disputes during travel; communication barriers on trips",
        "Teen":   "argument on a trip that becomes memorable; verbal conflict abroad",
        "Adult":  "business travel for verbal work — conferences, teaching, speaking; disputes abroad",
        "Middle": "international speaking or teaching; legal/contractual disputes across borders",
        "Senior": "continuing speaker circuit or teaching travel into retirement",
    },
    "Friends": {
        "Child":  "verbal sparring friendships; debate-oriented peer relationships",
        "Teen":   "friendships tested by arguments; verbal conflict periodic",
        "Adult":  "professional network of articulate people; disputes with colleagues",
        "Middle": "verbal feuds with former friends or colleagues; reputation-based rivalries",
        "Senior": "old verbal conflicts may finally resolve or stay bitter",
    },
    "Career": {
        "Teen":   "first work involves speaking/arguing — debate, journalism, tutoring, customer service",
        "Adult":  "lawyer, teacher, writer, broadcaster, critic, therapist, translator, preacher",
        "Middle": "senior legal, academic, media, or advisory role; respected voice in field",
        "Senior": "continued speaking, writing, or advisory work in retirement",
    },
    "Property": {
        "Child":  "family home has verbal arguments in it; discussion-heavy household",
        "Teen":   "household is argumentative; home is where debates happen",
        "Adult":  "legal disputes over property; contract issues with real estate",
        "Middle": "property disputes with family or neighbors; legal battles over real estate",
        "Senior": "estate disputes possible; legal complications with property transfer",
    },
    "Fortune": {
        "Child":  "verbal gift recognized early; speech contests, debate prizes",
        "Teen":   "verbal ability opens doors — scholarships, admissions through writing or speech",
        "Adult":  "luck through speaking and writing; reputation made through articulation",
        "Middle": "verbal legacy recognized; books, speeches, or legal wins become assets",
        "Senior": "lifetime of verbal work yields recognized reputation",
    },
    "Parents": {
        "Child":  "critical parents; verbal discipline; household has sharp-tongued figures",
        "Teen":   "parental criticism intensifies teen conflict; verbal battles at home",
        "Adult":  "continued verbal relationship with parent; critique remains a dynamic",
        "Middle": "aging parent's critical voice persists; verbal conflicts continue",
        "Senior": "parent's verbal legacy — both wounds and wisdom — comes into focus",
    },
},

# ═══════════════════════════════════════════════════════════
# TIAN XIANG — Heavenly Minister (WATER) — service, support, ministry
# ═══════════════════════════════════════════════════════════
"tian_xiang": {
    "Life": {
        "Child":  "helpful child; takes care of others; mediator in family conflicts",
        "Teen":   "supportive friend; counselor role among peers; puts others first",
        "Adult":  "service-oriented career; supports leaders rather than leading; diplomatic reputation",
        "Middle": "established supporter; reliable second-in-command; trusted advisor type",
        "Senior": "respected for lifetime of service; gentle elder",
    },
    "Siblings": {
        "Child":  "supportive with siblings; takes care of younger ones",
        "Teen":   "friend group counselor; helps others through their issues",
        "Adult":  "supportive in professional peer network; reliable collaborator",
        "Middle": "trusted among peers for reliability; mediator role",
        "Senior": "long-term supportive friendships remain",
    },
    "Spouse": {
        "Teen":   "first relationship with helpful, supportive partner or one who needs help",
        "Adult":  "marries supportive partner; mutual support is defining quality of union",
        "Middle": "partnership defined by mutual support; roles are helper and helped",
        "Senior": "long supportive marriage; caregiving in final decades",
    },
    "Children": {
        "Adult":  "nurturing parent; child may need extra support or be naturally supportive",
        "Middle": "supports teenage children through challenges; available parent",
        "Senior": "adult children remain supported; grandchildren receive gentle involvement",
    },
    "Wealth": {
        "Child":  "family money from service industries — administration, medicine, teaching, support roles",
        "Teen":   "first earnings from service work — administrative, hospitality, caregiving",
        "Adult":  "income through supporting roles — admin, HR, medical, paralegal, assistant, advisor",
        "Middle": "wealth from long-term support career; stable though not extravagant",
        "Senior": "modest but comfortable wealth from career of service",
    },
    "Health": {
        "Child":  "generally healthy; caretaker role may affect own wellbeing",
        "Teen":   "stable health; stress from putting others first",
        "Adult":  "health stable but overwork from service to others risks burnout",
        "Middle": "health issues from chronic overgiving; compassion fatigue",
        "Senior": "health in later years reflects lifetime of caregiving; gentle decline",
    },
    "Travel": {
        "Child":  "family travels to help relatives; service-oriented trips",
        "Teen":   "mission trips, volunteer travel, service-oriented journeys",
        "Adult":  "work travel in support of others' events; relocation to help family",
        "Middle": "moves to support aging parents, adult children, grandchildren; caregiving relocations",
        "Senior": "travel in later years is service-oriented or visiting those helped",
    },
    "Friends": {
        "Child":  "friends rely on this child; caretaker role in play groups",
        "Teen":   "everyone's therapist among friends; supportive role in group",
        "Adult":  "friends come for support; reliable friend in group",
        "Middle": "network of people supported over years; mutual support system",
        "Senior": "people helped over decades return support in later life",
    },
    "Career": {
        "Teen":   "first work in supporting role — assistant, volunteer, hospitality, caregiver",
        "Adult":  "administration, HR, medicine, ministry, secretary, advisor, counselor, paralegal",
        "Middle": "senior support role; chief of staff, senior advisor, administrator",
        "Senior": "continued service in volunteer, advisory, or ministry capacity",
    },
    "Property": {
        "Child":  "family home is gathering place for relatives; extended family stays often",
        "Teen":   "household often hosts relatives in need; open-door policy",
        "Adult":  "buys functional home; size reflects ability to host or help family",
        "Middle": "home accommodates aging parents or adult children; multi-generational capacity",
        "Senior": "home remains gathering place for family; passes to caregiver child",
    },
    "Fortune": {
        "Child":  "supported by others' generosity; helped along through childhood by adults",
        "Teen":   "mentors appear to help with next steps; supported into opportunities",
        "Adult":  "fortune through being helpful — opportunities come through service",
        "Middle": "lifetime of supporting others yields reliable blessings in return",
        "Senior": "those supported over lifetime return care in later years",
    },
    "Parents": {
        "Child":  "supportive parents; nurturing, service-oriented household",
        "Teen":   "parents model service to family, community, or faith",
        "Adult":  "continued supportive parents; adult relationship remains mutual",
        "Middle": "aging parents require support; role reversal gentle",
        "Senior": "parents fully supported in final years; gentle end-of-life caregiving",
    },
},

# ═══════════════════════════════════════════════════════════
# TIAN LIANG — Celestial Beam (EARTH) — elder protection, shelter, institutional support
# ═══════════════════════════════════════════════════════════
"tian_liang": {
    "Life": {
        "Child":  "old soul; wise beyond years; protected by grandparents or elders",
        "Teen":   "mature teen; counsels younger peers; elder mentors recognize them",
        "Adult":  "protected by institutions, mentors, elders; wise personality attracts guidance",
        "Middle": "becomes the elder for others; trusted counsel; protective authority",
        "Senior": "respected elder; longevity; fulfills full elder role",
    },
    "Siblings": {
        "Child":  "eldest-child energy regardless of birth order; protective with younger",
        "Teen":   "protective of friends; the responsible one in peer group",
        "Adult":  "mentor role with younger peers or siblings; guidance giver",
        "Middle": "elder statesman among peer group; trusted by younger colleagues",
        "Senior": "respected elder in peer network; consulted for wisdom",
    },
    "Spouse": {
        "Teen":   "first partner is older, wiser, or more established",
        "Adult":  "marries older partner or wiser one; protected marriage",
        "Middle": "partnership has protective quality; one supports the other",
        "Senior": "long marriage into old age; mutual care in final years",
    },
    "Children": {
        "Adult":  "protective, sheltering parenting; child well-protected from harm",
        "Middle": "continues protective role with teens; guides them through challenges",
        "Senior": "protective grandparent; guides grandchildren through long view",
    },
    "Wealth": {
        "Child":  "family money comes through institutions (pensions, government, inheritance)",
        "Teen":   "financial support from grandparents or elder mentors",
        "Adult":  "income through protective institutions — government, medicine, religion, insurance",
        "Middle": "wealth preserved through conservative management; protected assets",
        "Senior": "pensions, annuities, protected wealth serves final decades",
    },
    "Health": {
        "Child":  "recovers well from illness; longevity constitution evident early",
        "Teen":   "resilient health; protected by good habits or family care",
        "Adult":  "longevity constitution; recovers well from setbacks; protective health habits",
        "Middle": "preventive health focus pays off; protective approach to aging",
        "Senior": "longevity — lives notably long; recovers from later-life illnesses",
    },
    "Travel": {
        "Child":  "family travels to visit grandparents or elder relatives; pilgrimages",
        "Teen":   "protected travel — parents or institutions guide trip; mission or study abroad",
        "Adult":  "purposeful travel with protective institution — work, religion, education",
        "Middle": "pilgrimage or meaningful return trips; elder-sanctioned travel",
        "Senior": "travel to visit family and memorial sites in later years",
    },
    "Friends": {
        "Child":  "befriends older children or adult figures; mentored early",
        "Teen":   "connections with teachers, coaches, elder mentors",
        "Adult":  "mentor relationships with senior professionals; elders take interest",
        "Middle": "becomes mentor to others; mentor relationships flow both directions",
        "Senior": "remains connected to intergenerational community",
    },
    "Career": {
        "Teen":   "first work in protective institution — religious, medical, educational setting",
        "Adult":  "medicine, government, religion, education, insurance, elder care — protective fields",
        "Middle": "senior role in protective institution; respected within field",
        "Senior": "emeritus, advisory, or ceremonial role; wisdom transferred",
    },
    "Property": {
        "Child":  "family home inherited or has generational history; grandparents' home significant",
        "Teen":   "family home is protected asset; no major disruptions during teen years",
        "Adult":  "inherits property or buys home with long-term stability focus",
        "Middle": "preserves family property; multi-generational real estate planning",
        "Senior": "passes home to next generation with clear structure; estate legacy clear",
    },
    "Fortune": {
        "Child":  "protected from harm; sheltered childhood; disasters averted",
        "Teen":   "guided through teen dangers by mentors or institutions",
        "Adult":  "fortune through protection — disasters avoided, mentors intervene",
        "Middle": "luck through protective connections and conservative choices",
        "Senior": "later life blessed by protection; major illnesses survived, disasters avoided",
    },
    "Parents": {
        "Child":  "strong grandparent influence; sheltered upbringing; elder wisdom in household",
        "Teen":   "grandparents' influence significant; shielded from some family difficulties",
        "Adult":  "parents age but remain protective presence; wisdom transmitted",
        "Middle": "caregiving for aging parents; parents' longevity is theme",
        "Senior": "parents lived long lives; elder wisdom integrated",
    },
},

# ═══════════════════════════════════════════════════════════
# QI SHA — Seven Killings (METAL) — destruction, crisis, survival
# (Previously drafted, repeating here as part of complete file)
# ═══════════════════════════════════════════════════════════
"qi_sha": {
    "Life": {
        "Child":  "harsh parenting or absent protector; early exposure to family conflict or physical danger",
        "Teen":   "reputation as intense or intimidating; first serious physical risk (sports injury, accident, fight)",
        "Adult":  "identified professionally as crisis-handler; confrontation becomes defining event",
        "Middle": "surgery, accident, or forced simplification; pared-down lifestyle after major event",
        "Senior": "major surgery or health crisis; forced physical limitations reshape identity",
    },
    "Siblings": {
        "Child":  "sibling or close peer gets seriously hurt, leaves family, or dominates the child",
        "Teen":   "peer group fractures through betrayal, fight, or expulsion; friend's crisis reshapes group",
        "Adult":  "business partner exits under conflict; sibling faces serious illness or legal trouble",
        "Middle": "business breakup; sibling's health crisis or death; old peer group no longer functional",
        "Senior": "death, illness, or estrangement of sibling; loss of lifelong peer",
    },
    "Spouse": {
        "Child":  "parents' marriage in visible conflict or divorce; one parent absent",
        "Teen":   "first serious relationship ends in real rupture — not drifting apart",
        "Adult":  "marriage tested by crisis (infidelity, health scare, financial shock); partner undergoes major life event",
        "Middle": "divorce, spouse's serious illness, or relationship transformed under extreme pressure",
        "Senior": "spouse faces serious illness or surgery; widowhood or forced separation",
    },
    "Children": {
        "Teen":   "unexpected pregnancy, pregnancy complication, or creative project destroyed",
        "Adult":  "child faces accident or surgery; fertility struggle, miscarriage, or behavioral crisis",
        "Middle": "teen child undergoes major crisis (legal, health, mental health); caregiver burden shifts",
        "Senior": "adult child's life rupture requires parent's involvement; grandchild illness",
    },
    "Wealth": {
        "Child":  "family financial crisis — foreclosure, bankruptcy, forced move, parent job loss",
        "Teen":   "major money loss or gain through aggressive risk; first big financial shock",
        "Adult":  "business failure, lawsuit costs, forced asset sale; OR aggressive gain through risk",
        "Middle": "major asset lost in divorce, lawsuit, or business collapse; OR windfall through calculated aggression",
        "Senior": "medical bills consume savings; major asset sold under pressure",
    },
    "Health": {
        "Child":  "accident, broken bone, surgery, or acute illness requiring hospitalization",
        "Teen":   "sports injury, car accident, appendix/tonsils, first major medical procedure",
        "Adult":  "surgery, acute condition requiring operation, serious injury from accident",
        "Middle": "major surgery (cardiac, cancer), fall with fracture, or serious acute crisis",
        "Senior": "stroke, heart event, cancer diagnosis, or major organ surgery",
    },
    "Travel": {
        "Child":  "family forced move due to job loss, divorce, or crisis; loses school and friends mid-year",
        "Teen":   "moves abroad alone, study abroad crisis, accident while traveling",
        "Adult":  "job relocation requiring full uproot; forced expat move; crisis-driven relocation",
        "Middle": "move for aging parents, divorce forces relocation, or career pivot requires full move",
        "Senior": "medical evacuation, forced move for care, travel cut short by emergency",
    },
    "Friends": {
        "Child":  "best friend leaves or betrays; bullying or exclusion from group",
        "Teen":   "friend group collapses through conflict, betrayal, or a friend's crisis",
        "Adult":  "professional network rupture, falling out with mentor, key ally becomes adversary",
        "Middle": "falling out with longtime friend or colleague; key alliance dissolves acrimoniously",
        "Senior": "close friend dies, old community dissolves, lifelong friendship ends",
    },
    "Career": {
        "Teen":   "first job under harsh boss, military enlistment, dangerous work, or fired from first job",
        "Adult":  "fired, demoted, or forced resignation; OR aggressive pivot into law enforcement, surgery, military, demolition",
        "Middle": "forced out of position, company restructuring eliminates role; OR final major pivot",
        "Senior": "forced retirement, company collapse takes pension, final career reinvention",
    },
    "Property": {
        "Child":  "family loses home (foreclosure, eviction, disaster); house damage affecting child",
        "Teen":   "dorm/apartment conflict forces move; fire, flood, or theft at residence",
        "Adult":  "property demolition/major renovation, forced sale, natural disaster damage",
        "Middle": "divorce property dispute, major home renovation crisis, contested real estate",
        "Senior": "sells family home under pressure; property lost in estate dispute",
    },
    "Fortune": {
        "Child":  "family undergoes defining crisis that reshapes child's future (death, divorce, ruin, relocation)",
        "Teen":   "near-death experience, surviving an accident, event that changes life direction",
        "Adult":  "the year things break open — job loss leads to real calling, health scare forces priority reset",
        "Middle": "midlife crisis event that genuinely redirects remaining decades",
        "Senior": "survival of major medical event becomes defining story of later years",
    },
    "Parents": {
        "Child":  "parent's serious illness, accident, job loss, or crisis defines the year",
        "Teen":   "parental divorce, parent's surgery, death in extended family, financial collapse at home",
        "Adult":  "parent's surgery or major diagnosis; one parent's crisis demands caregiving",
        "Middle": "parent dies or requires full-time care; inheritance event; sibling conflict over parent care",
        "Senior": "both parents gone or fully dependent; eldest-generation transition",
    },
},

# ═══════════════════════════════════════════════════════════
# PO JUN — Army Breaker (WATER) — demolition, revolution, rebuilding
# ═══════════════════════════════════════════════════════════
"po_jun": {
    "Life": {
        "Child":  "disruptive or pioneering child; breaks conventions; unconventional path visible early",
        "Teen":   "rebels against family or school norms; reinvents self multiple times during teen years",
        "Adult":  "career or identity pivots dramatically; burns bridges to build new path",
        "Middle": "major midlife reinvention; starts over in new field or location",
        "Senior": "retirement itself is a reinvention; old life structures dissolved",
    },
    "Siblings": {
        "Child":  "peer groups shift repeatedly; friendships break and reform in childhood",
        "Teen":   "revolutionary peer group dynamics; friend groups completely replace each other",
        "Adult":  "co-founders split; business partnerships end dramatically; peer circle transformed",
        "Middle": "old peer group replaced entirely; new cohort formed around reinvention",
        "Senior": "lifelong friendships may end; new connections form in retirement",
    },
    "Spouse": {
        "Teen":   "dramatic first relationship breakup; relationship ends and reformats future romantic pattern",
        "Adult":  "marriage and divorce possible in sequence; dramatic relationship rebuilding",
        "Middle": "midlife divorce and remarriage; partnership demolished and rebuilt",
        "Senior": "late-life partnership change — widowhood followed by new relationship, or late divorce",
    },
    "Children": {
        "Adult":  "child with unconventional trajectory; parenting requires breaking with tradition",
        "Middle": "teen child breaks with family expectations; revolutionary parent-child dynamic",
        "Senior": "adult child takes radical life path; parent adapts or estranges",
    },
    "Wealth": {
        "Child":  "family wealth cycles dramatically — boom and bust; financial reset events",
        "Teen":   "first financial experience is dramatic — unexpected loss or unexpected gain",
        "Adult":  "boom-bust earning pattern; startup successes and failures; high variance",
        "Middle": "major financial restart — bankruptcy recovery, pivot to new field, asset restructure",
        "Senior": "late-life financial restructure; estate planning requires rebuilding from earlier disruptions",
    },
    "Health": {
        "Child":  "health crises followed by recovery cycles; dramatic illness and return to health",
        "Teen":   "health pattern of crisis and recovery; possibly breaking old health habits",
        "Adult":  "health crises requiring lifestyle demolition and rebuilding — body reset events",
        "Middle": "major health reset — surgery followed by lifestyle overhaul; body rebuilt",
        "Senior": "health crises followed by recovery arc; body proves resilient through demolition",
    },
    "Travel": {
        "Child":  "family relocations dramatic — cross-country, international, major uproot",
        "Teen":   "dramatic travel moments — runaway, emergency travel, unexpected extended trip",
        "Adult":  "permanent departures — leaves home country, cuts ties, doesn't return",
        "Middle": "major relocation reshapes second half of life — new country, new city, full uproot",
        "Senior": "final major move; leaving long-term residence for entirely new place",
    },
    "Friends": {
        "Child":  "friend groups dissolve and reform; dramatic social shifts through childhood",
        "Teen":   "peer network restarts repeatedly; friend group entirely replaced over teen years",
        "Adult":  "professional network demolished and rebuilt in each career pivot",
        "Middle": "old friendships dissolve; new peer group formed around new identity",
        "Senior": "late-life community rebuilding; new friends made in retirement after old ones lost",
    },
    "Career": {
        "Teen":   "first jobs end dramatically — fired, quit, industry collapse; restart pattern begins",
        "Adult":  "career reinvention is pattern; startup founder, demolition, restructuring, serial pivoter",
        "Middle": "major midlife career change — entirely new field; not promotion but revolution",
        "Senior": "retirement reinvention — second career, pivot into entirely new activity",
    },
    "Property": {
        "Child":  "family home renovated dramatically or family moves to very different place",
        "Teen":   "family home sold and rebuilt, or teen moves to radically different environment",
        "Adult":  "buys property requiring demolition and rebuild; flipping pattern; property revolutions",
        "Middle": "major property change — sells established home, radical renovation, fundamental housing restart",
        "Senior": "final property change — downsizing, moving to entirely different environment",
    },
    "Fortune": {
        "Child":  "family upheaval that reshapes trajectory — disaster, breakthrough, or radical change",
        "Teen":   "identity-reshaping event — conversion, radical influence, dramatic opportunity",
        "Adult":  "fortune through upheaval — bankruptcy leads to new path, crisis reveals calling",
        "Middle": "midlife destruction leads to authentic rebuild; the crisis becomes the gift",
        "Senior": "late-life reset reveals unexpected new direction; endings as beginnings",
    },
    "Parents": {
        "Child":  "parents broke from tradition or have unconventional history; non-traditional upbringing",
        "Teen":   "family structure changes dramatically — divorce, remarriage, new family members",
        "Adult":  "parents experience dramatic late-life changes — reinvention, remarriage, radical shift",
        "Middle": "parent's death reshapes family structure; inheritance triggers demolition/rebuild",
        "Senior": "parent's passing completes generational reset; family identity transformed",
    },
},

}


# ═══════════════════════════════════════════════════════════
# HELPER FUNCTION
# ═══════════════════════════════════════════════════════════

def get_age_bracket(age: int) -> str:
    """Map numeric age to age bracket."""
    if age <= 12:
        return "Child"
    elif age <= 19:
        return "Teen"
    elif age <= 39:
        return "Adult"
    elif age <= 59:
        return "Middle"
    else:
        return "Senior"


def get_star_palace_age_effect(star_pinyin: str, palace_english: str, age: int) -> str:
    """
    Get the age-specific interpretation for a star in a palace.
    Returns empty string if combination doesn't apply (e.g. Children palace for a child).
    """
    bracket = get_age_bracket(age)
    star_effects = STAR_PALACE_AGE_EFFECTS.get(star_pinyin, {})
    palace_effects = star_effects.get(palace_english, {})
    return palace_effects.get(bracket, "")
