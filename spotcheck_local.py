import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"C:\Users\allen\sl_zwds")
sys.path.insert(0, ".")
from datetime import datetime
from app.chart_builder import build_chart
from app.serializer import serialize_chart
from event_signals import compute_event_signals

chart = build_chart(birth_dt=datetime(1984, 4, 1, 19, 0), longitude=108.44,
                    latitude=11.94, tz_offset_hours=7.0, is_male=True, school="feixing")
p = serialize_chart(chart)
ann = {a["year"]: a for a in p["annuals"]}

for yr in (2022, 2023):
    a = ann[yr]
    es = compute_event_signals(a, a["age"])
    print(f"\n{'='*70}\n{yr} ({a['year_stem_branch']}, age {a['age']}, xs {a['age_xusui']})"
          + ("  PIVOTAL" if es["is_pivotal"] else ""))
    print(f"  LN-Ming on natal {a['palace_name_english']}")
    for c in es["classes"]:
        print(f"  {c['score']:5.1f} {c['class']:20s} {c['direction']}")
        for ev in c["evidence"][:3]:
            print(f"         - {ev}")
    # Friends role detail
    wheel = {w["role_english"]: w for w in a["annual_wheel"]}
    fr = wheel["Friends"]
    print(f"  LN-Friends = natal {fr['natal_palace_english']}: {' '.join(fr['stars'])}")
    for layer in ("decade", "annual"):
        for e in a["sihua_activations"][layer]:
            if e["annual_role"]["role_english"] in ("Friends", "Siblings"):
                print(f"    {layer} {e['type']} {e['star']} -> LN-{e['annual_role']['role_english']} (natal {e['natal_palace_english']})")
