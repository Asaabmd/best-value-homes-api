from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------- Demo dataset (add/replace with provider later) --------
DEMO_PROPERTIES = [
    {
        "id":"p1", "address":"2164 Noonday Ct, Henderson, NV 89052",
        "mode":"purchase", "price":978000, "rent":None,
        "beds":4, "baths":3.0, "sqft":3000, "lotSqft":9100,
        "singleStory":True, "garageStalls":3, "ownerParking":3, "guestParking":2,
        "hasPool":False, "hoaMonthly":87, "floodRisk":"minimal",
        "homeType":"SFH", "ageRestricted55":False, "petsAllowed":"either",
        "view":"valley", "updated":True, "yearBuilt":2001,
        "access_stepFree":True, "access_wideDoors":True, "access_walkInShower":True,
        "avoidBusyRoad":True, "culDeSac":True, "endUnit":False, "noRearNeighbor":True,
        "nearElementary":True, "evReady":True, "conditionBand":"turnkey",
        "photoUrl":"https://picsum.photos/seed/2164/600/400", "detailsUrl":"https://example.com/noonday",
        "singleFamilyTrafficQuiet":True
    },
    {
        "id":"p2", "address":"1501 Via Salaria Ct, Henderson, NV 89052",
        "mode":"purchase", "price":825000, "rent":None,
        "beds":4, "baths":2.5, "sqft":3050, "lotSqft":7405,
        "singleStory":True, "garageStalls":3, "ownerParking":3, "guestParking":1,
        "hasPool":False, "hoaMonthly":138, "floodRisk":"minimal",
        "homeType":"SFH", "ageRestricted55":False, "petsAllowed":"either",
        "view":None, "updated":True, "yearBuilt":1999,
        "access_stepFree":True, "access_wideDoors":False, "access_walkInShower":True,
        "avoidBusyRoad":True, "culDeSac":True, "endUnit":False, "noRearNeighbor":False,
        "nearElementary":True, "evReady":False, "conditionBand":"turnkey",
        "photoUrl":"https://picsum.photos/seed/1501/600/400", "detailsUrl":"https://example.com/viasalaria",
        "singleFamilyTrafficQuiet":True
    },
    {
        "id":"p3", "address":"1174 Mirage Lake St, Henderson, NV 89052",
        "mode":"purchase", "price":799000, "rent":None,
        "beds":4, "baths":3.0, "sqft":2680, "lotSqft":6970,
        "singleStory":True, "garageStalls":3, "ownerParking":3, "guestParking":1,
        "hasPool":False, "hoaMonthly":55, "floodRisk":"minimal",
        "homeType":"SFH", "ageRestricted55":False, "petsAllowed":"either",
        "view":None, "updated":True, "yearBuilt":1998,
        "access_stepFree":True, "access_wideDoors":False, "access_walkInShower":False,
        "avoidBusyRoad":True, "culDeSac":False, "endUnit":False, "noRearNeighbor":False,
        "nearElementary":True, "evReady":False, "conditionBand":"turnkey",
        "photoUrl":"https://picsum.photos/seed/1174/600/400", "detailsUrl":"https://example.com/miragelake",
        "singleFamilyTrafficQuiet":True
    },
    {
        "id":"p4", "address":"3020 Via Della Amore, Henderson, NV 89052",
        "mode":"purchase", "price":835000, "rent":None,
        "beds":4, "baths":3.0, "sqft":2550, "lotSqft":7405,
        "singleStory":True, "garageStalls":3, "ownerParking":3, "guestParking":2,
        "hasPool":False, "hoaMonthly":60, "floodRisk":"minimal",
        "homeType":"SFH", "ageRestricted55":False, "petsAllowed":"either",
        "view":"park", "updated":False, "yearBuilt":1999,
        "access_stepFree":True, "access_wideDoors":False, "access_walkInShower":False,
        "avoidBusyRoad":True, "culDeSac":False, "endUnit":False, "noRearNeighbor":True,
        "nearElementary":True, "evReady":False, "conditionBand":"light_reno",
        "photoUrl":"https://picsum.photos/seed/3020/600/400", "detailsUrl":"https://example.com/viadellaamore",
        "singleFamilyTrafficQuiet":True
    },
    {
        "id":"p5", "address":"2587 Grizzly Park Ct, Henderson, NV 89052",
        "mode":"purchase", "price":810000, "rent":None,
        "beds":4, "baths":3.0, "sqft":2679, "lotSqft":7405,
        "singleStory":True, "garageStalls":3, "ownerParking":3, "guestParking":1,
        "hasPool":False, "hoaMonthly":40, "floodRisk":"minimal",
        "homeType":"SFH", "ageRestricted55":False, "petsAllowed":"either",
        "view":None, "updated":False, "yearBuilt":1997,
        "access_stepFree":False, "access_wideDoors":False, "access_walkInShower":False,
        "avoidBusyRoad":True, "culDeSac":True, "endUnit":False, "noRearNeighbor":False,
        "nearElementary":True, "evReady":False, "conditionBand":"light_reno",
        "photoUrl":"https://picsum.photos/seed/2587/600/400", "detailsUrl":"https://example.com/grizzlypark",
        "singleFamilyTrafficQuiet":True
    },
    # Example rental (to show dual-mode)
    {
        "id":"r1", "address":"231 Serenity Walk, Henderson, NV 89052",
        "mode":"rent", "price":None, "rent":2850,
        "beds":3, "baths":2.0, "sqft":1850, "lotSqft":4500,
        "singleStory":True, "garageStalls":2, "ownerParking":2, "guestParking":1,
        "hasPool":False, "hoaMonthly":0, "floodRisk":"minimal",
        "homeType":"SFH", "ageRestricted55":True, "petsAllowed":"yes",
        "view":None, "updated":True, "yearBuilt":2005,
        "access_stepFree":True, "access_wideDoors":True, "access_walkInShower":True,
        "avoidBusyRoad":True, "culDeSac":False, "endUnit":False, "noRearNeighbor":False,
        "nearElementary":False, "evReady":False, "conditionBand":"turnkey",
        "photoUrl":"https://picsum.photos/seed/serenity/600/400", "detailsUrl":"https://example.com/serenity",
        "singleFamilyTrafficQuiet":True
    },
]

# ---------- Scoring ----------
def score_property(p, comps_ppsf=(260, 300), crit=None):
    score = 0
    pros, cons = [], []

    # Core fit
    if p.get("singleStory"): score += 8
    else: score += 2
    if p.get("garageStalls", 0) >= 3: score += 8
    if not p.get("hasPool"): score += 6
    if (p.get("hoaMonthly") or 0) <= (crit.get("hoaMax", 400) if crit else 400): score += 5
    if p.get("floodRisk") in ("minimal", "low"): score += 6
    if p.get("view"): score += 6; pros.append("Desirable view/setting")
    if p.get("updated"): score += 10; pros.append("Updated/turnkey")

    # Preferences
    if crit:
        if crit.get("ageRestricted55") == "yes" and p.get("ageRestricted55"): score += 5
        if crit.get("ageRestricted55") == "no" and p.get("ageRestricted55"): cons.append("55+ restricted")
        if p.get("ownerParking",0) >= crit.get("ownerParkingMin",0): score += 3
        if p.get("guestParking",0) >= crit.get("guestParkingMin",0): score += 2
        if crit.get("petsAllowed") == "yes" and str(p.get("petsAllowed")) == "yes": score += 3
        if crit.get("evReady") and p.get("evReady"): score += 2
        if crit.get("nearElementary") and p.get("nearElementary"): score += 2
        # Accessibility
        if crit.get("access_stepFree") and p.get("access_stepFree"): score += 2
        if crit.get("access_wideDoors") and p.get("access_wideDoors"): score += 2
        if crit.get("access_walkInShower") and p.get("access_walkInShower"): score += 2
        # Privacy/noise
        if crit.get("culDeSac") and p.get("culDeSac"): score += 2
        if crit.get("endUnit") and p.get("endUnit"): score += 1
        if crit.get("noRearNeighbor") and p.get("noRearNeighbor"): score += 2
        # Lot size
        if p.get("lotSqft") and p["lotSqft"] >= crit.get("minLotSqft", 0): score += 2

    # Price vs comps (purchase only)
    ppsf = None
    bench = sum(comps_ppsf)/2
    if p.get("price") and p.get("sqft"):
        ppsf = p["price"] / max(p["sqft"], 1)
        if ppsf <= bench * 0.95: score += 10; pros.append("Priced below comps")
        elif ppsf >= bench * 1.10: cons.append("Priced above comps")

    # Bath note
    if p.get("baths", 0) < (crit.get("minBaths", 0) if crit else 3): cons.append("Fewer baths than requested")

    return {
        "id": p["id"],
        "property": p,
        "valueScore": min(100, round(score, 1)),
        "pros": pros or ["Matches key criteria"],
        "cons": cons,
        "pricePerSqft": round(ppsf, 2) if ppsf else None,
        "compRange": f"${comps_ppsf[0]}/sf–${comps_ppsf[1]}/sf (3–6 mo comps)"
    }

# ---------- Search ----------
@app.post("/search")
def search():
    """
    Accepts budget-only or full criteria.
    Key fields:
      mode: "purchase" | "rent"
      stories: "single" | "two" | "either"
      ageRestricted55: "yes" | "no" | "either"
      petsAllowed: "yes" | "no" | "either"
      homeTypes: ["SFH","Townhome","Condo"]
      ownerParkingMin, guestParkingMin (ints)
      accessibility flags, privacy flags, minLotSqft, nearElementary, evReady
    """
    crit = request.get_json() or {}
    # Defaults
    mode = crit.get("mode", "purchase")
    zip_code = crit.get("zip", "89052")
    max_price = crit.get("maxPrice", 1_000_000)
    max_rent  = crit.get("maxRent", 10**9)
    min_price = crit.get("minPrice", 0)
    min_beds  = crit.get("minBeds", 4 if mode=="purchase" else 2)
    min_baths = crit.get("minBaths", 3.0 if mode=="purchase" else 2.0)
    stories_pref = crit.get("stories", "either")
    home_types = set(crit.get("homeTypes", ["SFH","Townhome","Condo"]))
    hoa_max = crit.get("hoaMax", 400)
    no_pool = crit.get("noPool", True)
    no_flood = crit.get("excludeFlood", True)

    # Optional flags
    def passes_common(p):
        if zip_code not in p["address"]: return False
        if p.get("homeType") not in home_types: return False
        # Mode-specific budget
        if mode == "purchase":
            if p.get("mode") != "purchase": return False
            if p.get("price") is None or p["price"] > max_price or p["price"] < min_price: return False
        else:
            if p.get("mode") != "rent": return False
            if p.get("rent") is None or p["rent"] > max_rent: return False

        # Beds/Baths/Size
        if p.get("beds", 0) < min_beds: return False
        if p.get("baths", 0) < min_baths: return False
        if crit.get("minSqft") and p.get("sqft", 0) < crit["minSqft"]: return False

        # Stories
        if stories_pref == "single" and not p.get("singleStory", False): return False
        if stories_pref == "two" and p.get("singleStory", False): return False

        # 55+
        ar = crit.get("ageRestricted55", "either")
        if ar == "yes" and not p.get("ageRestricted55"): return False
        if ar == "no" and p.get("ageRestricted55"): return False

        # Parking
        if p.get("ownerParking",0) < crit.get("ownerParkingMin",0): return False
        if p.get("guestParking",0) < crit.get("guestParkingMin",0): return False

        # Pets
        pets = crit.get("petsAllowed","either")
        if pets != "either" and str(p.get("petsAllowed","either")) != pets: return False

        # HOA/Pool/Flood
        if p.get("hoaMonthly") and p["hoaMonthly"] > hoa_max: return False
        if no_pool and p.get("hasPool"): return False
        if no_flood and p.get("floodRisk") not in ("minimal","low"): return False

        # Accessibility
        if crit.get("access_stepFree") and not p.get("access_stepFree"): return False
        if crit.get("access_wideDoors") and not p.get("access_wideDoors"): return False
        if crit.get("access_walkInShower") and not p.get("access_walkInShower"): return False

        # Lot & privacy/noise
        if crit.get("minLotSqft") and (p.get("lotSqft") or 0) < crit["minLotSqft"]: return False
        if crit.get("avoidBusyRoad") and not p.get("avoidBusyRoad", False): return False
        if crit.get("culDeSac") and not p.get("culDeSac", False): return False
        if crit.get("endUnit") and not p.get("endUnit", False): return False
        if crit.get("noRearNeighbor") and not p.get("noRearNeighbor", False): return False

        # Schools
        if crit.get("nearElementary") and not p.get("nearElementary", False): return False

        # EV
        if crit.get("evReady") and not p.get("evReady", False): return False

        # Condition band (turnkey / light_reno / heavy_reno)
        cond = crit.get("conditionBand")
        if cond and p.get("conditionBand") not in ([cond] if isinstance(cond, str) else cond): return False

        # Radius omitted (demo)
        return True

    # Progressive widen if empty (keep ethics: still respect flood/pool)
    widen_steps = [
        lambda p: passes_common(p),
        lambda p: passes_common(p),  # relax rules here later if needed
    ]

    candidates = []
    for step in widen_steps:
        for p in DEMO_PROPERTIES:
            if step(p) and p not in candidates:
                candidates.append(p)
        if len(candidates) >= 5:
            break

    # Market background (stubbed; replace with real analytics later)
    comps_ppsf = (260, 300)
    purchase_range = {"low": 675000, "high": 705000, "ppsfLow": 260, "ppsfHigh": 300}
    rent_range = {"low": 2600, "high": 3100}
    trend = {"direction":"flat","pct":0.0,"domChange":-2}

    scored = [score_property(p, comps_ppsf, crit) for p in candidates]
    scored.sort(key=lambda x: x["valueScore"], reverse=True)
    if scored:
        scored[0]["isBestValue"] = True

    # Budget hint
    low_ppsf, high_ppsf = comps_ppsf
    if mode == "purchase":
        max_price_eff = max_price
        est_low_sf  = int(max_price_eff / high_ppsf)
        est_high_sf = int(max_price_eff / low_ppsf)
        budgetAdvice = {"maxPrice": max_price_eff, "typicalSqftRange": f"{est_low_sf}–{est_high_sf} sf at ${low_ppsf}-${high_ppsf}/sf comps"}
    else:
        budgetAdvice = {"maxRent": max_rent, "typicalRentRange": f"${rent_range['low']:,}–${rent_range['high']:,}/mo (similar rentals)"}

    return jsonify({
        "marketBackground": {
            "purchaseCompRange": purchase_range,
            "rentRange": rent_range,
            "trend": trend
        },
        "budgetAdvice": budgetAdvice,
        "results": scored[:5]
    })

# ---------- Follow-up Q&A (stub) ----------
@app.post("/followup")
def followup():
    """
    Body: { "propertyId":"p1", "question":"Is there an HOA capital contribution?" }
    Returns a simple, safe, templated answer from known fields. Replace with LLM later if desired.
    """
    data = request.get_json() or {}
    pid = data.get("propertyId")
    q = (data.get("question") or "").strip()
    prop = next((x for x in DEMO_PROPERTIES if x["id"] == pid), None)
    if not prop:
        return jsonify({"answer":"Sorry, I couldn't find that property."}), 404

    bits = []
    bits.append(f"Address: {prop['address']}")
    if prop.get("mode") == "purchase":
        bits.append(f"List price: ${prop['price']:,}")
        if prop.get("sqft"): bits.append(f"Size: {prop['sqft']} sf (${round(prop['price']/prop['sqft'])}/sf approx.)")
    else:
        bits.append(f"Monthly rent: ${prop['rent']:,}")
        if prop.get("sqft"): bits.append(f"Size: {prop['sqft']} sf")

    bits.append(f"{prop['beds']} bed / {prop['baths']} bath • {'1-story' if prop['singleStory'] else '2-story'} • {prop.get('garageStalls',0)}-car garage")
    if prop.get("hoaMonthly") is not None: bits.append(f"HOA: ${prop['hoaMonthly']}/mo")
    bits.append(f"Pool: {'No' if not prop.get('hasPool') else 'Yes'} • Flood risk: {prop.get('floodRisk','unknown')}")
    if prop.get("ageRestricted55"): bits.append("55+ community")
    if prop.get("petsAllowed") != "either": bits.append(f"Pets: {prop['petsAllowed']}")
    if prop.get("evReady"): bits.append("EV-ready")
    if prop.get("nearElementary"): bits.append("Near elementary")

    preface = "Here’s what I can confirm from the listing. For anything not listed, I recommend messaging the listing agent via the Details link."
    return jsonify({
        "answer": preface + " " + " • ".join(bits),
        "detailsUrl": prop.get("detailsUrl")
    })

@app.get("/")
def root():
    return jsonify({"ok": True, "message": "Best-Value Homes API running."})
