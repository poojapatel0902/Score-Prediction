import pandas as pd
import numpy as np
import pickle
from xgboost import XGBRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# 1. Load the raw level 2 data
print("Loading data...")
df = pickle.load(open('dataset_level2.pkl','rb'))

# --- FIX 1: Convert Data Types to Numbers ---
df['match_id'] = pd.to_numeric(df['match_id'], errors='coerce')
df['runs'] = pd.to_numeric(df['runs'], errors='coerce')
df['ball'] = pd.to_numeric(df['ball'], errors='coerce')
df.dropna(subset=['match_id', 'runs'], inplace=True)

# 2. FEATURE ENGINEERING
teams = [
    'Australia', 'Bangladesh', 'England', 'India', 'New Zealand',
    'Pakistan', 'South Africa', 'Sri Lanka', 'West Indies', 'Afghanistan'
]
df = df[df['batting_team'].isin(teams)]
df = df[df['bowling_team'].isin(teams)]

# Calculate Current Score (Now works because runs is numeric)
df['current_score'] = df.groupby('match_id')['runs'].cumsum()

# Calculate Balls Left
df['over'] = df['ball'].apply(lambda x: str(x).split(".")[0]).astype(int)
df['ball_no'] = df['ball'].apply(lambda x: str(x).split(".")[1] if '.' in str(x) else 0).astype(int)
df['balls_bowled'] = (df['over'] * 6) + df['ball_no']
df['balls_left'] = 120 - df['balls_bowled']
df['balls_left'] = df['balls_left'].apply(lambda x: 0 if x < 0 else x)

# Calculate Wickets Left
df['player_dismissed'] = df['player_dismissed'].apply(lambda x: 0 if x == '0' or x == 0 else 1)
df['wickets_fallen'] = df.groupby('match_id')['player_dismissed'].cumsum()
df['wickets_left'] = 10 - df['wickets_fallen']

# Calculate Current Run Rate (CRR)
df['crr'] = (df['current_score'] * 6) / df['balls_bowled']

# --- FIX 2: Calculate Target (runs_x) correctly ---
total_runs_df = df.groupby('match_id')['runs'].sum().reset_index()
total_runs_df.rename(columns={'runs': 'runs_x'}, inplace=True)
final_df = df.merge(total_runs_df, on='match_id')

# --- FIX 3: Correct Rolling Sum for last_5_over ---
final_df['last_5_over'] = final_df.groupby('match_id')['runs'].rolling(window=30).sum().values.tolist()

# Final Selection
final_df = final_df[['batting_team','bowling_team','city','current_score','balls_left','wickets_left','crr','last_5_over','runs_x']]
final_df.dropna(inplace=True)

# 3. Split X and y
X = final_df.drop(columns=['runs_x'])
y = final_df['runs_x']

# 4. Pipeline setup
trf = ColumnTransformer([
    ('trf', OneHotEncoder(sparse_output=False, drop='first'), 
     ['batting_team', 'bowling_team', 'city'])
], remainder='passthrough')

pipe = Pipeline(steps=[
    ('step1', trf),
    ('step2', XGBRegressor(n_estimators=1000, learning_rate=0.2, max_depth=12, random_state=42))
])

# 5. Fit and Save
print("Training started... this will take a moment...")
pipe.fit(X, y)
pickle.dump(pipe, open('pipe.pkl', 'wb'))
print("Success! pipe.pkl is created and ready for app.py")