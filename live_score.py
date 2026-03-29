import requests
import streamlit as st

# ── RapidAPI Config ──────────────────────────────────────────
RAPIDAPI_HOST = "free-cricbuzz-cricket-api.p.rapidapi.com"
BASE_URL      = f"https://{RAPIDAPI_HOST}"

# ── Team Maps ────────────────────────────────────────────────
IPL_TEAMS = {
    "Chennai Super Kings":        ["Chennai Super Kings", "CSK"],
    "Delhi Capitals":             ["Delhi Capitals", "DC"],
    "Gujarat Titans":             ["Gujarat Titans", "GT"],
    "Kolkata Knight Riders":      ["Kolkata Knight Riders", "KKR"],
    "Lucknow Super Giants":       ["Lucknow Super Giants", "LSG"],
    "Mumbai Indians":             ["Mumbai Indians", "MI"],
    "Punjab Kings":               ["Punjab Kings", "PBKS"],
    "Rajasthan Royals":           ["Rajasthan Royals", "RR"],
    "Royal Challengers Bengaluru":["Royal Challengers Bengaluru", "RCB",
                                   "Royal Challengers Bangalore"],
    "Sunrisers Hyderabad":        ["Sunrisers Hyderabad", "SRH"],
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
        "X-RapidAPI-Key":  get_api_key(),
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "Content-Type":    "application/json",
    }

def match_team_name(api_team, team_dict):
    """API team name → model team name"""
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
    """Fetch all live T20 / IPL matches from RapidAPI Cricbuzz"""
    api_key = get_api_key()
    if not api_key:
        return [], "API Key nahi mili. Streamlit Secrets mein RAPIDAPI_KEY set karo."

    try:
        url = f"{BASE_URL}/cricket-match-live-score"     # live matches endpoint
        response = requests.get(url, headers=get_headers(), timeout=10)

        # ── If endpoint gives 404 / empty, try fixtures ───────
        if response.status_code == 404 or not response.text.strip():
            url = f"{BASE_URL}/cricket-fixtures"
            response = requests.get(url, headers=get_headers(), timeout=10)

        data = response.json()

        # API returns list directly OR wrapped in a key
        if isinstance(data, list):
            all_matches = data
        elif isinstance(data, dict):
            # Try common wrapper keys
            all_matches = (data.get("matches")
                        or data.get("data")
                        or data.get("results")
                        or [])
        else:
            all_matches = []

        if not all_matches:
            return [], None          # No error — just no live matches right now

        # Filter IPL / T20
        filtered = []
        for m in all_matches:
            series     = str(m.get("series",    "")).lower()
            match_type = str(m.get("matchType", "")).lower()
            name       = str(m.get("name",      "")).lower()

            is_ipl = "ipl" in series or "indian premier" in series or "ipl" in name
            is_t20 = "t20" in match_type or "t20" in series or "t20" in name

            if is_ipl or is_t20:
                m["is_ipl"] = is_ipl
                filtered.append(m)

        return filtered, None

    except requests.exceptions.Timeout:
        return [], "Request timeout — internet check karo."
    except Exception as e:
        return [], f"Error: {str(e)}"


# ── Live Score for One Match ──────────────────────────────────
def get_match_live_score(match_id):
    """Fetch live scorecard for a specific match"""
    api_key = get_api_key()
    if not api_key:
        return None, "API Key nahi mili."

    try:
        url = f"{BASE_URL}/cricket-match-info"
        params = {"matchid": match_id}
        response = requests.get(url, headers=get_headers(),
                                params=params, timeout=10)
        data = response.json()

        # ── Unwrap response ───────────────────────────────────
        if isinstance(data, dict):
            scorecard = (data.get("scorecard")
                      or data.get("data")
                      or data.get("score")
                      or data)
        else:
            scorecard = {}

        # ── Extract runs / wickets / overs ───────────────────
        # Try nested score list first
        scores = scorecard.get("score", [])
        if scores and isinstance(scores, list):
            current = scores[0]
            runs    = int(current.get("r", 0))
            wickets = int(current.get("w", 0))
            overs_raw = str(current.get("o", "0.0"))
        else:
            # Flat structure
            runs      = int(scorecard.get("runs",    data.get("runs",    0)))
            wickets   = int(scorecard.get("wickets", data.get("wickets", 0)))
            overs_raw = str(scorecard.get("overs",   data.get("overs",   "0.0")))

        # ── Parse overs (e.g. "12.3" → 12.3) ────────────────
        try:
            parts         = overs_raw.split(".")
            full_overs    = int(parts[0])
            balls         = int(parts[1]) if len(parts) > 1 else 0
            overs_decimal = round(full_overs + balls / 10, 1)
        except Exception:
            overs_decimal = 0.0

        # ── Team names ────────────────────────────────────────
        teams = scorecard.get("teams", [])
        if teams and isinstance(teams, list):
            batting_raw = teams[0]
            bowling_raw = teams[1] if len(teams) > 1 else ""
        else:
            batting_raw = (scorecard.get("batting") or data.get("battingTeam", ""))
            bowling_raw = (scorecard.get("bowling") or data.get("bowlingTeam", ""))

        result = {
            "runs":             runs,
            "wickets":          wickets,
            "overs":            overs_decimal,
            "batting_team_raw": batting_raw,
            "bowling_team_raw": bowling_raw,
            "match_name":       (scorecard.get("name")
                              or data.get("matchName")
                              or data.get("name", "Live Match")),
            "status":           (scorecard.get("status")
                              or data.get("status", "")),
        }
        return result, None

    except requests.exceptions.Timeout:
        return None, "Timeout — dubara try karo."
    except Exception as e:
        return None, f"Error: {str(e)}"