# Score Predictor 

## Objective
The  Score Predictor is a dynamic, machine learning-driven web application designed to forecast the first-innings score of both Indian Premier League (IPL) and International T20 matches. Featuring an intelligent, context-aware user interface, the application seamlessly adapts its prediction models and input parameters based on the user's selected tournament.

## Dataset
<a href= "https://github.com/poojapatel0902/Score-Prediction/tree/main/ipl%20score%20prediction/ipl">ipl dataset</a>


## Project Process
1. Dual-Pipeline Data Engineering
Processed and cleaned two massive, distinct datasets: one for historical IPL matches and another for International T20s.
Engineered critical dynamic features for both formats, including balls_left, wickets_left, and current_run_rate (CRR), while incorporating format-specific metrics like the last_5_over momentum for international games.
2. Dynamic Machine Learning Architecture
Trained two separate XGBoost Regressor models to capture the unique scoring patterns, pitch behaviors, and team dynamics of franchise cricket (IPL) versus international cricket (T20).
Implemented dynamic model loading (ipl_pipe.pkl vs. t20_pipe.pkl) in the backend, ensuring high accuracy based on the tournament context.
3. Context-Aware UI/UX Development
Built a highly interactive frontend using Streamlit.
Dynamic Routing: Engineered a smart selection system where choosing the tournament (IPL or T20) instantly populates the respective batting/bowling teams and specific host cities without reloading the page.
Designed a premium, responsive "Dark Glassmorphism" UI using custom CSS for a visually striking experience on both mobile and desktop.
4. Cloud Deployment
Deployed the unified application to Streamlit Cloud, managing multiple serialized models and ensuring low-latency predictions.

localhost: streamlit run app.py

## Live Application: scorecast.streamlit.app

## Project Insights
Franchise vs. International Dynamics: The models reveal that IPL scoring is heavily influenced by specific high-altitude or historically high-scoring Indian grounds (like Bengaluru), whereas International T20s show a stronger reliance on recent batting momentum (last_5_over feature).
The Wicket Multiplier: Across both formats, wickets in hand during the final 5 overs have an exponentially higher impact on the projected final score than the current run rate alone.
Early Overs Volatility: Predictions made within the Powerplay rely heavily on the batting team's historical strength and venue, while predictions in the middle overs shift heavily toward the current_run_rate and wickets_left.

## Conclusion
This project successfully merges two complex machine learning pipelines into a single, intuitive web application. By combining highly accurate XGBoost prediction models with a smart, dynamically updating frontend, this tool transforms complex predictive analytics into a seamless user experience. It stands as a testament to end-to-end full-stack data science—from managing multiple datasets and models to deploying a polished, context-aware web app
