import requests
import streamlit as st

# ── FREE API — No Key Needed! ─────────────────────────────────
# Source: https://github.com/ekamid/cricbuzz-live
BASE_URL = "https://cricbuzz-live.vercel.app/v1"

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
        url = f"{BASE_URL}/matches/live"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return [], f"API Error: Status {response.status_code}"

        data = response.json()
        all_matches = data.get("data", {}).get("matches", [])

        if not all_matches:
            return [], None

        # Filter IPL / T20 matches
        filtered = []
        for m in all_matches:
            title = m.get("title", "")
            if is_ipl_match(title):
                m["is_ipl"] = True
                filtered.append(m)

        # Agar koi IPL match na mile — saare T20 matches dikhao
        if not filtered:
            filtered = all_matches  # Sab dikhao

        return filtered, None

    except requests.exceptions.Timeout:
        return [], "Timeout — dubara try karo."
    except Exception as e:
        return [], f"Error: {str(e)}"

# ── Live Score for One Match ──────────────────────────────────
def get_match_live_score(match_id):
    try:
        url = f"{BASE_URL}/score/{match_id}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None, f"Score fetch nahi hua: Status {response.status_code}"

        data = response.json()
        score_data = data.get("data", {})

        # Parse live score string e.g. "MI 87/2 (10.3 Ovs)"
        live_score_str = score_data.get("liveScore", "0/0 (0.0 Ovs)")

        runs, wickets, overs_decimal = 0, 0, 0.0
        try:
            # "MI 87/2 (10.3 Ovs)" → extract runs/wickets/overs
            import re
            rw_match = re.search(r'(\d+)/(\d+)', live_score_str)
            ov_match = re.search(r'\((\d+\.\d+)', live_score_str)

            if rw_match:
                runs    = int(rw_match.group(1))
                wickets = int(rw_match.group(2))
            if ov_match:
                overs_decimal = float(ov_match.group(1))
        except Exception:
            pass

        # Teams from title
        title  = score_data.get("title", "Live Match")
        teams  = score_data.get("teams", [])

        batting_raw = teams[0].get("team", "") if teams and isinstance(teams[0], dict) else ""
        bowling_raw = teams[1].get("team", "") if len(teams) > 1 and isinstance(teams[1], dict) else ""

        # Agar teams empty hain — title se try karo
        if not batting_raw and "vs" in title.lower():
            parts       = title.lower().split("vs")
            batting_raw = parts[0].strip()
            bowling_raw = parts[1].strip().split(",")[0].strip()

        return {
            "runs":             runs,
            "wickets":          wickets,
            "overs":            overs_decimal,
            "batting_team_raw": batting_raw,
            "bowling_team_raw": bowling_raw,
            "match_name":       title,
            "status":           score_data.get("update", ""),
        }, None

    except requests.exceptions.Timeout:
        return None, "Timeout — dubara try karo."
    except Exception as e:
        return None, f"Error: {str(e)}"