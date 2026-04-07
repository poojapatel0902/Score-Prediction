import requests
import streamlit as st

# ── OFFICIAL CRICAPI (cricketdata.org) ───────────────────────
CRICKET_API_KEY = "4fced4fa-53da-4030-86f1-ab36a5820a56"
BASE_URL = "https://api.cricapi.com/v1"

# ── Team Maps ────────────────────────────────────────────────
IPL_TEAMS = {
    "Chennai Super Kings":         ["Chennai Super Kings", "CSK", "chennai"],
    "Delhi Capitals":              ["Delhi Capitals", "DC", "delhi"],
    "Gujarat Titans":              ["Gujarat Titans", "GT", "gujarat"],
    "Kolkata Knight Riders":       ["Kolkata Knight Riders", "KKR", "kolkata"],
    "Lucknow Super Giants":        ["Lucknow Super Giants", "LSG", "lucknow"],
    "Mumbai Indians":              ["Mumbai Indians", "MI", "mumbai"],
    "Punjab Kings":                ["Punjab Kings", "PBKS", "punjab"],
    "Rajasthan Royals":            ["Rajasthan Royals", "RR", "rajasthan"],
    "Royal Challengers Bengaluru": ["Royal Challengers Bengaluru", "RCB",
                                    "Royal Challengers Bangalore", "bangalore", "bengaluru"],
    "Sunrisers Hyderabad":         ["Sunrisers Hyderabad", "SRH", "hyderabad"],
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

# ── Helper ────────────────────────────────────────────────────
def match_team_name(api_team, team_dict):
    if not api_team:
        return None
    api_lower = api_team.lower()
    for model_name, aliases in team_dict.items():
        for alias in aliases:
            if alias.lower() in api_lower or api_lower in alias.lower():
                return model_name
    return None

def is_ipl_match(title):
    """Check if match title contains IPL team names"""
    title_lower = title.lower()
    ipl_keywords = [
        "csk", "mi ", "rcb", "kkr", "srh", "rr ", " dc ", "gt ", "pbks", "lsg",
        "chennai", "mumbai", "bangalore", "bengaluru", "kolkata",
        "hyderabad", "rajasthan", "delhi", "gujarat", "punjab", "lucknow",
        "ipl", "indian premier"
    ]
    return any(kw in title_lower for kw in ipl_keywords)

# ── Live Matches ──────────────────────────────────────────────
def get_live_matches():
    try:
        # Naya URL (currentMatches API)
        url = f"{BASE_URL}/currentMatches?apikey={CRICKET_API_KEY}&offset=0"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return [], f"API Error: Status {response.status_code}"

        data = response.json()
        
        # Check for API limit error
        if data.get("status") == "failure":
            return [], f"API Error: {data.get('reason', 'Daily Limit Reached')}"

        all_matches = data.get("data", [])

        if not all_matches:
            return [], None

        # Filter IPL / T20 matches
        filtered = []
        for m in all_matches:
            title = m.get("name", "")
            match_type = str(m.get("matchType", "")).lower()
            
            if match_type == "t20" or match_type == "t20i" or is_ipl_match(title):
                # Return format same as old code so app.py doesn't break
                m["title"] = title 
                m["is_ipl"] = is_ipl_match(title)
                filtered.append(m)

        # Agar koi match na mile — saare matches dikhao fallback ke liye
        if not filtered:
            for m in all_matches:
                m["title"] = m.get("name", "")
            filtered = all_matches

        return filtered, None

    except requests.exceptions.Timeout:
        return [], "Timeout — dubara try karo."
    except Exception as e:
        return [], f"Error: {str(e)}"

# ── Live Score for One Match ──────────────────────────────────
def get_match_live_score(match_id):
    try:
        # Naya URL (match_info API) for specific match
        url = f"{BASE_URL}/match_info?apikey={CRICKET_API_KEY}&id={match_id}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None, f"Score fetch nahi hua: Status {response.status_code}"

        data = response.json()
        
        if data.get("status") == "failure":
            return None, f"API Error: {data.get('reason', 'Daily Limit Reached')}"
            
        score_data = data.get("data", {})

        runs, wickets, overs_decimal = 0, 0, 0.0
        
        # CricAPI direct numbers deta hai (Regex ki zaroorat nahi)
        score_array = score_data.get("score", [])
        if score_array and len(score_array) > 0:
            latest_score = score_array[-1] # Latest inning score
            runs = latest_score.get("r", 0)
            wickets = latest_score.get("w", 0)
            overs_decimal = float(latest_score.get("o", 0.0))
            inning_str = latest_score.get("inning", "")
        else:
            inning_str = ""

        # Teams from API
        title = score_data.get("name", "Live Match")
        teams = score_data.get("teams", ["", ""])
        
        batting_raw = ""
        bowling_raw = ""

        if len(teams) >= 2:
            # Pata lagao kaun batting kar raha hai
            if teams[0] in inning_str:
                batting_raw = teams[0]
                bowling_raw = teams[1]
            elif teams[1] in inning_str:
                batting_raw = teams[1]
                bowling_raw = teams[0]
            else:
                # Fallback
                batting_raw = teams[0]
                bowling_raw = teams[1]

        # Wapas wahi dictionary bhejo jo app.py ko samajh aati hai
        return {
            "runs":             runs,
            "wickets":          wickets,
            "overs":            overs_decimal,
            "batting_team_raw": batting_raw,
            "bowling_team_raw": bowling_raw,
            "match_name":       title,
            "status":           score_data.get("status", ""),
        }, None

    except requests.exceptions.Timeout:
        return None, "Timeout — dubara try karo."
    except Exception as e:
        return None, f"Error: {str(e)}"