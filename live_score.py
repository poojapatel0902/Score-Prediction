import requests
import streamlit as st

# ── RapidAPI Config ──────────────────────────────────────────
RAPIDAPI_HOST = "free-cricbuzz-cricket-api.p.rapidapi.com"
BASE_URL      = f"https://{RAPIDAPI_HOST}"

# ── Team Maps ────────────────────────────────────────────────
IPL_TEAMS = {
    "Chennai Super Kings":         ["Chennai Super Kings", "CSK"],
    "Delhi Capitals":              ["Delhi Capitals", "DC"],
    "Gujarat Titans":              ["Gujarat Titans", "GT"],
    "Kolkata Knight Riders":       ["Kolkata Knight Riders", "KKR"],
    "Lucknow Super Giants":        ["Lucknow Super Giants", "LSG"],
    "Mumbai Indians":              ["Mumbai Indians", "MI"],
    "Punjab Kings":                ["Punjab Kings", "PBKS"],
    "Rajasthan Royals":            ["Rajasthan Royals", "RR"],
    "Royal Challengers Bengaluru": ["Royal Challengers Bengaluru", "RCB",
                                    "Royal Challengers Bangalore"],
    "Sunrisers Hyderabad":         ["Sunrisers Hyderabad", "SRH"],
}

T20_TEAMS = {
    "Australia":    ["Australia",    "AUS"],
    "Bangladesh":   ["Bangladesh",   "BAN"],
    "England":      ["England",      "ENG"],
    "India":        ["India",        "IND"],
    "New Zealand":  ["New Zealand",  "NZ", "NZL"],
    "Pakistan":     ["Pakistan",     "PAK"],
    "South Africa": ["South Africa", "SA", "RSA"],
    "Sri Lanka":    ["Sri Lanka",    "SL", "LKA"],
    "West Indies":  ["West Indies",  "WI"],
}

# ── Helpers ───────────────────────────────────────────────────
def get_api_key():
    try:
        return st.secrets["RAPIDAPI_KEY"]
    except Exception:
        return None

def get_headers():
    return {
        "x-rapidapi-key":  get_api_key(),
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

def match_team_name(api_team, team_dict):
    if not api_team:
        return None
    api_lower = api_team.lower()
    for model_name, aliases in team_dict.items():
        for alias in aliases:
            if alias.lower() in api_lower or api_lower in alias.lower():
                return model_name
    return None

# ── Live Matches ──────────────────────────────────────────────
def get_live_matches():
    api_key = get_api_key()
    if not api_key:
        return [], "API Key nahi mili. Streamlit Secrets mein RAPIDAPI_KEY set karo."

    headers = get_headers()

    # Try 3 possible endpoints — jo bhi kaam kare
    endpoints_to_try = [
        f"{BASE_URL}/cricket-match-live-score",
        f"{BASE_URL}/cricket-fixtures",
        f"{BASE_URL}/matches",
    ]

    raw_data = None
    worked_url = None

    for url in endpoints_to_try:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200 and r.text.strip():
                raw_data = r.json()
                worked_url = url
                break
        except Exception:
            continue

    if raw_data is None:
        return [], "API se koi response nahi aaya. RapidAPI key check karo."

    # ── Parse response — list ya dict dono handle karo ────────
    all_matches = []
    if isinstance(raw_data, list):
        all_matches = raw_data
    elif isinstance(raw_data, dict):
        for key in ["matches", "data", "results", "fixtures", "typeMatches"]:
            val = raw_data.get(key)
            if val and isinstance(val, list):
                all_matches = val
                break
        # Cricbuzz nested format: typeMatches > seriesMatches > matches
        if not all_matches:
            for section in raw_data.get("typeMatches", []):
                for series in section.get("seriesMatches", []):
                    series_card = series.get("seriesAdWrapper") or series
                    for m in series_card.get("matches", []):
                        all_matches.append(m.get("matchInfo", m))

    # ── Show raw response in sidebar for debugging ─────────────
    with st.sidebar:
        st.markdown("### 🔧 Debug Info")
        st.caption(f"URL tried: `{worked_url}`")
        st.caption(f"Total matches found: {len(all_matches)}")
        if all_matches:
            st.json(all_matches[0])   # Show first match structure

    if not all_matches:
        return [], None

    # ── Filter IPL / T20 ──────────────────────────────────────
    filtered = []
    for m in all_matches:
        # Handle nested matchInfo
        info = m.get("matchInfo", m)

        series     = str(info.get("seriesName", info.get("series",    ""))).lower()
        match_type = str(info.get("matchFormat", info.get("matchType",""))).lower()
        name       = str(info.get("matchDesc",   info.get("name",     ""))).lower()
        team1_raw  = info.get("team1", {})
        team2_raw  = info.get("team2", {})
        team1      = str(team1_raw.get("teamName","") if isinstance(team1_raw,dict) else team1_raw).lower()
        team2      = str(team2_raw.get("teamName","") if isinstance(team2_raw,dict) else team2_raw).lower()

        is_ipl = any(kw in series for kw in ["ipl", "indian premier"])
        is_t20 = "t20" in match_type or "t20" in series

        # Also check team names directly for IPL teams
        ipl_keywords = ["csk","mi","rcb","kkr","srh","rr","dc","gt","pbks","lsg",
                        "chennai","mumbai","bangalore","bengaluru","kolkata",
                        "hyderabad","rajasthan","delhi","gujarat","punjab","lucknow"]
        teams_str = team1 + " " + team2
        has_ipl_team = any(kw in teams_str for kw in ipl_keywords)

        if is_ipl or is_t20 or has_ipl_team:
            m["is_ipl"] = is_ipl or has_ipl_team
            m["_name"]  = name or f"{team1} vs {team2}"
            m["_id"]    = (info.get("matchId") or info.get("id") or
                           m.get("matchId")    or m.get("id", ""))
            filtered.append(m)

    return filtered, None


# ── Live Score for One Match ──────────────────────────────────
def get_match_live_score(match_id):
    api_key = get_api_key()
    if not api_key:
        return None, "API Key nahi mili."

    headers = get_headers()

    # Try both possible score endpoints
    urls_to_try = [
        (f"{BASE_URL}/cricket-match-info",        {"matchid": match_id}),
        (f"{BASE_URL}/cricket-match-live-score",  {"matchid": match_id}),
        (f"{BASE_URL}/match-scorecard",           {"id":      match_id}),
    ]

    data = None
    for url, params in urls_to_try:
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
            if r.status_code == 200 and r.text.strip():
                data = r.json()
                break
        except Exception:
            continue

    if data is None:
        return None, "Match ka score fetch nahi hua."

    # ── Unwrap ────────────────────────────────────────────────
    scorecard = (data.get("scorecard") or data.get("data") or
                 data.get("score")     or data)

    # ── Runs / Wickets / Overs ────────────────────────────────
    scores = scorecard.get("score", [])
    if scores and isinstance(scores, list):
        current = scores[0]
        runs    = int(current.get("r", 0))
        wickets = int(current.get("w", 0))
        overs_r = str(current.get("o", "0.0"))
    else:
        runs    = int(scorecard.get("runs",    data.get("runs",    0)))
        wickets = int(scorecard.get("wickets", data.get("wickets", 0)))
        overs_r = str(scorecard.get("overs",   data.get("overs",   "0.0")))

    # ── Parse overs ───────────────────────────────────────────
    try:
        parts         = overs_r.split(".")
        full_overs    = int(parts[0])
        balls         = int(parts[1]) if len(parts) > 1 else 0
        overs_decimal = round(full_overs + balls / 10, 1)
    except Exception:
        overs_decimal = 0.0

    # ── Teams ─────────────────────────────────────────────────
    teams = scorecard.get("teams", [])
    if teams and isinstance(teams, list):
        batting_raw = str(teams[0])
        bowling_raw = str(teams[1]) if len(teams) > 1 else ""
    else:
        batting_raw = str(scorecard.get("batting") or data.get("battingTeam", ""))
        bowling_raw = str(scorecard.get("bowling") or data.get("bowlingTeam", ""))

    return {
        "runs":             runs,
        "wickets":          wickets,
        "overs":            overs_decimal,
        "batting_team_raw": batting_raw,
        "bowling_team_raw": bowling_raw,
        "match_name":       (scorecard.get("name") or data.get("matchName")
                             or data.get("name", "Live Match")),
        "status":           (scorecard.get("status") or data.get("status", "")),
    }, None