import streamlit as st
import pickle
import pandas as pd
import base64
import time

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
            margin-bottom: 6px !important; /* <--- YAHAN CHANGE KIYA: Label ke niche 12px ki saans (space) de di */
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
           10. 📱 MOBILE AUR TABLET RESPONSIVE CSS
           ========================================= */
        @media screen and (max-width: 768px) {{
            h1.page-title {{
                font-size: 40 px !important; /* Have aa change thase */
                line-height: 1.2 !important;
            }}
            p, label {{
                font-size: 22px !important;
            }}
        }}

        /* 3. SMALL PHONES (480px and below) */
        /* Aa hamesha 768px ni niche rakhvu */
        @media screen and (max-width: 480px) {{
            h1.page-title {{
                font-size: 32px !important; 
            }}
            p, label {{
                font-size: 18px !important;
            }}
        }}
        
        /* Baaki no CSS (Background, Buttons etc.) am nam j rehva do */
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
    <h1 id="main-title" style="margin: 0; padding: 0;color: #ff9800;text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.9); font-size: 65px"> Score Predictor</h1>
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

# ---------------- UI (DABBE) ---------------- #
if "reset_count" not in st.session_state:
    st.session_state["reset_count"] = 0
rk = st.session_state["reset_count"]

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

# ---------------- PREDICTION LOGIC ---------------- #
if st.button("Predict Score"):
    if batting_team == bowling_team:
        st.error("Batting and Bowling team cannot be the same!")
    else:
        overs_completed = int(overs)
        balls_in_current_over = int(round((overs - overs_completed) * 10))
        balls_bowled = (overs_completed * 6) + balls_in_current_over

        balls_left = 120 - balls_bowled
        wickets_left = 10 - wickets

        # Calculate Run Rate
        run_rate_value = (current_score * 6) / balls_bowled if balls_bowled > 0 else 0

        # Aapke model ke hisaab se Dataframe columns set karna
        if tournament == "IPL":
            input_df = pd.DataFrame({
                "batting_team": [batting_team],
                "bowling_team": [bowling_team],
                "city": [city],
                "current_score": [current_score],
                "balls_left": [balls_left],
                "wickets_left": [wickets_left],
                "current_run_rate": [run_rate_value] # IPL needs 'current_run_rate'
            })
        else:
            input_df = pd.DataFrame({
                "batting_team": [batting_team],
                "bowling_team": [bowling_team],
                "city": [city],
                "current_score": [current_score],
                "balls_left": [balls_left],
                "wickets_left": [wickets_left],
                "current_run_rate": [run_rate_value], # T20 needs 'crr'
                "last_5_over": [0]       # T20 needs 'last_5_over'
            })

        # Predict
        result = pipe.predict(input_df)
        predicted_score = int(result[0])

        st.success(f"🏆 Predicted Final Score: {predicted_score}")
        
        
        # Timer & Refresh
        countdown_msg = st.empty()
        for i in range(10, 0, -1):
            countdown_msg.info(f"⏳ Page will refresh in {i} seconds ")
            time.sleep(1)
            
        st.session_state["reset_count"] += 1
        st.rerun()