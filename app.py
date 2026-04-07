# import warnings
# warnings.filterwarnings('ignore', category=UserWarning, module='xgboost')

# import streamlit as st
# import pickle
# import pandas as pd
# import base64
# import time
# from live_score import get_live_matches, get_match_live_score, match_team_name, IPL_TEAMS, T20_TEAMS
# st.set_page_config(page_title="Cricket Score Predictor", layout="wide")

# # ---------------- BACKGROUND AUR CSS ---------------- #
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as file:
#         encoded_string = base64.b64encode(file.read()).decode()
        
#     st.markdown(
#         f"""
#         <style>
#         /* BACKGROUND IMAGE AUR WHITE SPACE FIX */
#         .stApp::before {{
#             content: "";
#             background-image:linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(data:image/png;base64,{encoded_string});
#             background-size: cover;
#             background-attachment: fixed;
#             background-position: center top;
#             position: fixed;
#             top: 0; left: 0; right: 0; bottom: 0;
#             filter: blur(4px); 
#             z-index: -1;
#         }}
#         .stApp {{ background: transparent; }}
#         header[data-testid="stHeader"] {{ background: transparent !important; }}
#         header[data-testid="stHeader"] * {{ color: #FFFFFF !important; }}
        
#         /* HEADING (TITLE) */
#         #main-title {{
#             font-size: 65px !important; 
#             color: white !important;  
#             text-align: center;
#             text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.9) !important;
#             margin-top: 105px !important;
#         }}
        

#         /* BAAKI NORMAL TEXT (Labels) */
#         p, label {{
#             color: #FAFAFA!important; 
#             font-size: 25px !important;
#             font-weight: bold;
#             margin-bottom: 6px !important; /* <--- YAHAN CHANGE KIYA: Label ke niche 12px ki saans (space) de di */
#             display: inline-block !important;
#         }}

#         /* SAARE DABBE (Outer Box) KI TRANSPARENCY */
#         div[data-baseweb="select"] > div, 
#         div[data-testid="stNumberInputContainer"],
#         ul[role="listbox"] {{
#             background-color: rgba(255, 255, 255, 0.5)!important; 
#             border: 1px  rgba(255, 255, 255, 0.5) !important;
#             border-radius: 8px !important;
#             min-height: 45px ;
#             font-size: 20px;
#             color:black !important; 
#         }}

#         div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="input"] > div,
#         input, div[data-baseweb="select"] span, li[role="option"] {{
#             background-color: transparent !important; 
#             color: black !important; 
#             font-size: 20px !important; 
#             border: none !important;
#             box-shadow: none !important;
#         }}

#         div[data-testid="stNumberInputContainer"] button {{ display: none !important; }}
#         li[role="option"]:hover {{ background-color: rgba(0, 0, 0, 0.4) !important; color: white !important; }}

#         /* PREDICT BUTTON */
#         div.stButton > button {{
#             background: linear-gradient(90deg,#ff9800,#ff5722)!important; 
#             border: 2px  #FFD700 !important; 
#             width: 100%; height: 55px; margin-top: 25px;
#             padding: 20px !important; border-radius: 8px !important; 
#         }}
#         div.stButton > button p {{
#             color: #FFFFFF !important;  
#             font-size: 25px !important;
#             font-weight: bold !important;
#             margin: 0px !important;
#         }}
        
#         /* PAGE KO CENTER MEIN LANA */
#         .block-container {{
#             max-width: 1050px !important; 
#             padding-top: 15vh !important; 
#             padding-bottom: 2rem !important;
#         }}
        
        
#         div[data-testid="stAlert"] {{ background-color: rgba(225,225,225, 0.5) !important; border-radius: 8px !important; }}
#         div[data-testid="stAlert"] p {{ color: black !important; font-size: 22px !important; text-shadow: none !important; }}

#        /* =========================================
#            10. 📱 MOBILE AUR TABLET RESPONSIVE CSS
#            ========================================= */
#         @media screen and (max-width: 768px) {{
#             #main-title {{
#                 font-size: 45px !important; /* Ab space nahi hai aur id sahi hai */
#                 line-height: 1.2 !important;
#                 margin-top: 30px !important;
#             }}
#             p, label {{
#                 font-size: 22px !important;
#             }}
#         }}

#         /* 3. SMALL PHONES (480px and below) */
#         @media screen and (max-width: 480px) {{
#             #main-title {{
#                 font-size: 35px !important; /* Chhote phone ke liye perfect */
#                 margin-top: 10px !important;
#             }}
#             p, label {{
#                 font-size: 18px !important;
#             }}
#         }}
        
#         /* Baaki no CSS (Background, Buttons etc.) am nam j rehva do */
#         .stApp::before {{
#             content: "";
#             background-image: url(data:image/png;base64,{encoded_string});
#             background-size: cover;
#             background-attachment: fixed;
#             position: fixed;
#             top: 0; left: 0; right: 0; bottom: 0;
#             filter: blur(4px); 
#             z-index: -1;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# add_bg_from_local("image3.png")

# # ---------------- TOURNAMENT SELECTION ---------------- #
# st.markdown(f"""
# <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 10px; padding-bottom: 15px;">
#     <h1 id="main-title" style="margin: 0; padding: 0; color: #ff9800; text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.9);"> Score Predictor</h1>
# </div>
            
# """, unsafe_allow_html=True)

# tournament = st.selectbox(" Select Tournament ", ["IPL", "T20 "])


# # ---------------- DYNAMIC DATA & MODEL LOADING ---------------- #
# if tournament == "IPL":
#     pipe = pickle.load(open("ipl_pipe.pkl", "rb"))
#     teams = [
#         'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans',
#         'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians',
#         'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bengaluru',
#         'Sunrisers Hyderabad'
#     ]
#     cities = [
#         'Ahmedabad', 'Bengaluru', 'Chandigarh', 'Chennai', 'Delhi',
#         'Dharamsala', 'Hyderabad', 'Jaipur', 'Kolkata', 'Lucknow',
#         'Mumbai', 'Pune', 'Visakhapatnam'
#     ]
# else:
#     pipe = pickle.load(open("t20_pipe.pkl", "rb"))
#     teams = [
#         'Australia', 'Bangladesh', 'England', 'India', 'New Zealand', 
#         'Pakistan', 'South Africa', 'Sri Lanka', 'West Indies'
#     ]
#     cities = [
#        'Ahmedabad', 'Adelaide', 'Bengaluru', 'Birmingham', 'Bridgetown', 
#     'Colombo', 'Delhi', 'Hambantota', 'Hyderabad', 'Kandy', 'Kolkata', 
#     'London', 'Manchester', 'Melbourne', 'Mumbai', 'North Sound', 'Perth', 'Sydney'
#     ]

# # ---------------- UI (DABBE) ---------------- #
# if "reset_count" not in st.session_state:
#     st.session_state["reset_count"] = 0
# rk = st.session_state["reset_count"]

# col1, col2 = st.columns(2)
# with col1:
#     batting_team = st.selectbox("Select Batting Team", sorted(teams), key=f"bat_{rk}")
# with col2:
#     bowling_team = st.selectbox("Select Bowling Team", sorted(teams), key=f"bowl_{rk}")

# city = st.selectbox("Select City", sorted(cities), key=f"city_{rk}")

# col3, col4, col5 = st.columns(3)
# with col3:
#     current_score = st.number_input("Current Score", min_value=0, step=1, key=f"score_{rk}")
# with col4:
#     overs = st.number_input("Overs Bowled (e.g., 5.3)", min_value=5.0, max_value=19.5, step=0.1, key=f"overs_{rk}")
# with col5:
#     wickets = st.number_input("Wickets Fallen", min_value=0, max_value=10, step=1, key=f"wickets_{rk}")

# # ---------------- PREDICTION LOGIC ---------------- #
# if st.button("Predict Score"):
#     if batting_team == bowling_team:
#         st.error("Batting and Bowling team cannot be the same!")
#     else:
#         overs_completed = int(overs)
#         balls_in_current_over = int(round((overs - overs_completed) * 10))
#         balls_bowled = (overs_completed * 6) + balls_in_current_over

#         balls_left = 120 - balls_bowled
#         wickets_left = 10 - wickets

#         # Calculate Run Rate
#         run_rate_value = (current_score * 6) / balls_bowled if balls_bowled > 0 else 0

#         # Aapke model ke hisaab se Dataframe columns set karna
#         if tournament == "IPL":
#             input_df = pd.DataFrame({
#                 "batting_team": [batting_team],
#                 "bowling_team": [bowling_team],
#                 "city": [city],
#                 "current_score": [current_score],
#                 "balls_left": [balls_left],
#                 "wickets_left": [wickets_left],
#                 "current_run_rate": [run_rate_value] # IPL needs 'current_run_rate'
#             })
#         else:
#             input_df = pd.DataFrame({
#                 "batting_team": [batting_team],
#                 "bowling_team": [bowling_team],
#                 "city": [city],
#                 "current_score": [current_score],
#                 "balls_left": [balls_left],
#                 "wickets_left": [wickets_left],
#                 "current_run_rate": [run_rate_value], # T20 needs 'crr'
#                 "last_5_over": [0]       # T20 needs 'last_5_over'
#             })

#         # Predict
#         result = pipe.predict(input_df)
#         predicted_score = int(result[0])

#         st.success(f"🏆 Predicted Final Score: {predicted_score}")
        
        
#         # Timer & Refresh
#         countdown_msg = st.empty()
#         for i in range(10, 0, -1):
#             countdown_msg.info(f"⏳ Page will refresh in {i} seconds ")
#             time.sleep(1)
            
#         st.session_state["reset_count"] += 1
#         st.rerun()

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='xgboost')

import streamlit as st
import pickle
import pandas as pd
import base64
import time
from live_score import get_live_matches, get_match_live_score, match_team_name, IPL_TEAMS, T20_TEAMS

st.set_page_config(page_title="Cricket Score Predictor", layout="wide")

# ---------------- BACKGROUND AUR CSS ---------------- #
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
        
    st.markdown(
        f"""
        <style>
        /* BACKGROUND IMAGE AUR WHITE SPACE FIX */
        .stApp::before {{
            content: "";
            background-image:linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-attachment: fixed;
            background-position: center top;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            filter: blur(4px); 
            z-index: -1;
        }}
        .stApp {{ background: transparent; }}
        header[data-testid="stHeader"] {{ background: transparent !important; }}
        header[data-testid="stHeader"] * {{ color: #FFFFFF !important; }}
        
        /* HEADING (TITLE) */
        #main-title {{
            font-size: 65px !important; 
            color: white !important;  
            text-align: center;
            text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.9) !important;
            margin-top: 105px !important;
        }}

        /* BAAKI NORMAL TEXT (Labels) */
        p, label {{
            color: #FAFAFA!important; 
            font-size: 25px !important;
            font-weight: bold;
            margin-bottom: 6px !important;
            display: inline-block !important;
        }}

        /* SAARE DABBE (Outer Box) KI TRANSPARENCY */
        div[data-baseweb="select"] > div, 
        div[data-testid="stNumberInputContainer"],
        ul[role="listbox"] {{
            background-color: rgba(255, 255, 255, 0.5)!important; 
            border: 1px  rgba(255, 255, 255, 0.5) !important;
            border-radius: 8px !important;
            min-height: 45px ;
            font-size: 20px;
            color:black !important; 
        }}

        div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="input"] > div,
        input, div[data-baseweb="select"] span, li[role="option"] {{
            background-color: transparent !important; 
            color: black !important; 
            font-size: 20px !important; 
            border: none !important;
            box-shadow: none !important;
        }}

        div[data-testid="stNumberInputContainer"] button {{ display: none !important; }}
        li[role="option"]:hover {{ background-color: rgba(0, 0, 0, 0.4) !important; color: white !important; }}

        /* PREDICT BUTTON */
        div.stButton > button {{
            background: linear-gradient(90deg,#ff9800,#ff5722)!important; 
            border: 2px  #FFD700 !important; 
            width: 100%; height: 55px; margin-top: 25px;
            padding: 20px !important; border-radius: 8px !important; 
        }}
        div.stButton > button p {{
            color: #FFFFFF !important;  
            font-size: 25px !important;
            font-weight: bold !important;
            margin: 0px !important;
        }}
        
        /* PAGE KO CENTER MEIN LANA */
        .block-container {{
            max-width: 1050px !important; 
            padding-top: 15vh !important; 
            padding-bottom: 2rem !important;
        }}
        
        div[data-testid="stAlert"] {{ background-color: rgba(225,225,225, 0.5) !important; border-radius: 8px !important; }}
        div[data-testid="stAlert"] p {{ color: black !important; font-size: 22px !important; text-shadow: none !important; }}

        /* =========================================
           MOBILE AUR TABLET RESPONSIVE CSS
           ========================================= */
        @media screen and (max-width: 768px) {{
            #main-title {{
                font-size: 45px !important;
                line-height: 1.2 !important;
                margin-top: 30px !important;
            }}
            p, label {{
                font-size: 22px !important;
            }}
        }}

        @media screen and (max-width: 480px) {{
            #main-title {{
                font-size: 35px !important;
                margin-top: 10px !important;
            }}
            p, label {{
                font-size: 18px !important;
            }}
        }}
        
        .stApp::before {{
            content: "";
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-attachment: fixed;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            filter: blur(4px); 
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("image3.png")

# ---------------- TOURNAMENT SELECTION ---------------- #
st.markdown(f"""
<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 10px; padding-bottom: 15px;">
    <h1 id="main-title" style="margin: 0; padding: 0; color: #ff9800; text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.9);"> Score Predictor</h1>
</div>
""", unsafe_allow_html=True)

tournament = st.selectbox(" Select Tournament ", ["IPL", "T20 "])

# ---------------- DYNAMIC DATA & MODEL LOADING ---------------- #
if tournament == "IPL":
    pipe = pickle.load(open("ipl_pipe.pkl", "rb"))
    teams = [
        'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans',
        'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians',
        'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bengaluru',
        'Sunrisers Hyderabad'
    ]
    cities = [
        'Ahmedabad', 'Bengaluru', 'Chandigarh', 'Chennai', 'Delhi',
        'Dharamsala', 'Hyderabad', 'Jaipur', 'Kolkata', 'Lucknow',
        'Mumbai', 'Pune', 'Visakhapatnam'
    ]
else:
    pipe = pickle.load(open("t20_pipe.pkl", "rb"))
    teams = [
        'Australia', 'Bangladesh', 'England', 'India', 'New Zealand', 
        'Pakistan', 'South Africa', 'Sri Lanka', 'West Indies'
    ]
    cities = [
        'Ahmedabad', 'Adelaide', 'Bengaluru', 'Birmingham', 'Bridgetown', 
        'Colombo', 'Delhi', 'Hambantota', 'Hyderabad', 'Kandy', 'Kolkata', 
        'London', 'Manchester', 'Melbourne', 'Mumbai', 'North Sound', 'Perth', 'Sydney'
    ]

# ================================================================
# 🔴 LIVE MATCH SECTION
# ================================================================

if "live_data" not in st.session_state:
    st.session_state.live_data = None
if "auto_filled" not in st.session_state:
    st.session_state.auto_filled = False


live_toggle = st.toggle(" Auto-Fill", value=False, key="live_toggle")

if live_toggle:
    with st.spinner(" Live matches searching..."):
        live_matches, err = get_live_matches()

    if err:
        st.error(f"❌ {err}")
    elif not live_matches:
        st.warning("There is no live match.")
    else:
        match_labels = {}
        for m in live_matches:
            name  = m.get("_name") or m.get("title") or m.get("name", "Unknown Match")
            m_id  = m.get("_id")  or m.get("id", "")
            emoji = " IPL" if m.get("is_ipl") else "T20"
            label = f"{emoji} — {name}"
            if m_id:
                match_labels[label] = m_id

        if not match_labels:
            st.warning(" Match list mili but ID nahi mili. Thodi der baad try karo.")
        else:
            selected_label = st.selectbox(
                " Select Live Match ",
                list(match_labels.keys()),
                key="live_match_select"
            )
            selected_id = match_labels[selected_label]

            col_fetch, col_refresh = st.columns([1, 1])
            with col_fetch:
                fetch_btn = st.button("Score Fetching ", key="fetch_live")
            with col_refresh:
                auto_refresh = st.checkbox("Auto-Refresh (30 sec)", value=False, key="auto_refresh")

            if fetch_btn or auto_refresh:
                live_data, score_err = get_match_live_score(selected_id)

                if score_err:
                    st.error(f"❌ {score_err}")
                elif live_data:
                    st.session_state.live_data  = live_data
                    st.session_state.auto_filled = True

                    # Live Scoreboard Card
                    runs = live_data['runs']
                    wkts = live_data['wickets']
                    ovrs = live_data['overs']
                    crr  = round(runs / max(float(ovrs), 0.1), 2)

                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(30,30,30,0.8));
                        border-radius: 15px; padding: 20px;
                        border: 2px  #ff9800; margin: 10px 0;
                        text-align: center;
                    ">
                        <p style="color:#ff9800; font-size:18px; margin:0;">🔴 LIVE</p>
                        <h2 style="color:white; margin:5px 0;">{live_data['match_name']}</h2>
                        <div style="display:flex; justify-content:space-around; margin-top:15px;">
                            <div style="color:white;">
                                <div style="font-size:32px; font-weight:bold;">{runs}/{wkts}</div>
                                <div style="color:#aaa; font-size:14px;">Score</div>
                            </div>
                            <div style="color:white;">
                                <div style="font-size:32px; font-weight:bold;">{ovrs}</div>
                                <div style="color:#aaa; font-size:14px;">Overs</div>
                            </div>
                            <div style="color:white;">
                                <div style="font-size:32px; font-weight:bold;">{crr}</div>
                                <div style="color:#aaa; font-size:14px;">CRR</div>
                            </div>
                        </div>
                        
                    </div>
                    """, unsafe_allow_html=True)

                    if auto_refresh:
                        placeholder = st.empty()
                        for t in range(30, 0, -1):
                            placeholder.caption(f"🔄 {t} sec mein score update hoga...")
                            time.sleep(1)
                        st.rerun()



# ================================================================
# 🎯 SESSION STATE AUTO-FILL LOGIC
# ================================================================
if "reset_count" not in st.session_state:
    st.session_state["reset_count"] = 0
rk = st.session_state["reset_count"]

# Agar live data aagaya hai, toh input boxes ko force-update karo
if st.session_state.auto_filled and st.session_state.live_data:
    d = st.session_state.live_data
    team_dict = IPL_TEAMS if tournament == "IPL" else T20_TEAMS

    mapped_bat  = match_team_name(d['batting_team_raw'],  team_dict)
    mapped_bowl = match_team_name(d['bowling_team_raw'], team_dict)

    # Widgets ki keys ko update kar rahe hain
    st.session_state[f"score_{rk}"] = int(d['runs'])
    st.session_state[f"overs_{rk}"] = max(float(d['overs']), 5.0)
    st.session_state[f"wickets_{rk}"] = int(d['wickets'])

    if mapped_bat and mapped_bat in teams:
        st.session_state[f"bat_{rk}"] = mapped_bat
    if mapped_bowl and mapped_bowl in teams:
        st.session_state[f"bowl_{rk}"] = mapped_bowl


# ================================================================
# ORIGINAL UI (DABBE) - Bina kisi UI change ke
# ================================================================
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("Select Batting Team", sorted(teams), key=f"bat_{rk}")
with col2:
    bowling_team = st.selectbox("Select Bowling Team", sorted(teams), key=f"bowl_{rk}")

city = st.selectbox("Select City", sorted(cities), key=f"city_{rk}")

col3, col4, col5 = st.columns(3)
with col3:
    current_score = st.number_input("Current Score", min_value=0, step=1, key=f"score_{rk}")
with col4:
    overs = st.number_input("Overs Bowled (e.g., 5.3)", min_value=5.0, max_value=19.5, step=0.1, key=f"overs_{rk}")
with col5:
    wickets = st.number_input("Wickets Fallen", min_value=0, max_value=10, step=1, key=f"wickets_{rk}")


# ---------------- PREDICTION LOGIC — ORIGINAL CODE ---------------- #
if st.button("Predict Score"):
    if batting_team == bowling_team:
        st.error("Batting and Bowling team cannot be the same!")
    else:
        overs_completed       = int(overs)
        balls_in_current_over = int(round((overs - overs_completed) * 10))
        balls_bowled          = (overs_completed * 6) + balls_in_current_over
        balls_left            = 120 - balls_bowled
        wickets_left          = 10 - wickets
        run_rate_value        = (current_score * 6) / balls_bowled if balls_bowled > 0 else 0

        if tournament == "IPL":
            input_df = pd.DataFrame({
                "batting_team":    [batting_team],
                "bowling_team":    [bowling_team],
                "city":            [city],
                "current_score":   [current_score],
                "balls_left":      [balls_left],
                "wickets_left":    [wickets_left],
                "current_run_rate":[run_rate_value]
            })
        else:
            input_df = pd.DataFrame({
                "batting_team":    [batting_team],
                "bowling_team":    [bowling_team],
                "city":            [city],
                "current_score":   [current_score],
                "balls_left":      [balls_left],
                "wickets_left":    [wickets_left],
                "current_run_rate":[run_rate_value],
                "last_5_over":     [0]
            })

        result          = pipe.predict(input_df)
        predicted_score = int(result[0])
        st.success(f"🏆 Predicted Final Score: {predicted_score}")

        countdown_msg = st.empty()
        for i in range(10, 0, -1):
            countdown_msg.info(f"⏳ Page will refresh in {i} seconds ")
            time.sleep(1)

        st.session_state.auto_filled        = False
        st.session_state.live_data          = None
        st.session_state["reset_count"]    += 1
        st.rerun()