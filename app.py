# app.py

import streamlit as st
import openai
import os
import re
import hashlib


# At the very top of your app.py
import streamlit as st

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''


# Set your OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')


# Define user credentials (username: hashed_password)
USER_CREDENTIALS = {
    'user1': hashlib.sha256('password1'.encode()).hexdigest(),
    'user2': hashlib.sha256('password2'.encode()).hexdigest(),
    # Add more users as needed
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    hashed_password = hash_password(password)
    stored_password = USER_CREDENTIALS.get(username)
    if stored_password and hashed_password == stored_password:
        return True
    else:
        return False

def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login", key="login_button")
    
    if login_button:
        if authenticate(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            # Set a flag to trigger rerun
            st.session_state['just_logged_in'] = True
            # st.success(f"Logged in as {username}")
        else:
            st.error("Invalid username or password")


def logout():
    st.session_state['authenticated'] = False
    st.session_state['username'] = ''
    st.session_state['just_logged_out'] = True
    # st.sidebar.info("You have been logged out.")



def fetch_token_data(token_name):
    # Mocked token data
    data = {
        'name': token_name,
        'symbol': 'SYM',
        'market_cap': '100M',
        'team': 'Anonymous',
        'social_media': {
            'twitter_followers': 5000,
            'reddit_subscribers': 2000
        },
        'transactions': {
            'holders': 1500,
            'transactions_last_24h': 300
        }
    }
    return data

def analyze_token(token_name):
    token_data = fetch_token_data(token_name)
    
    prompt = f"""
    Analyze the following token data and determine the likelihood that the token is a scam. Provide reasons for your assessment.

    Token Data:
    {token_data}

    Provide your analysis below, and conclude with 'Scam Likelihood: XX%'.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a crypto analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    analysis = response['choices'][0]['message']['content']
    return analysis

def display_results(analysis):
    st.header("Analysis Result")
    st.write(analysis)

def extract_scam_likelihood(analysis_text):
    match = re.search(r'Scam Likelihood:\s*(\d+)%', analysis_text)
    if match:
        return int(match.group(1))
    else:
        return 50

def execute_trade(token_name):
    st.write(f"Executing trade for {token_name}...")
    st.write("Trade executed successfully!")

def main():
    # Check for login/logout events and trigger reruns
    if st.session_state.get('just_logged_in'):
        del st.session_state['just_logged_in']
        st.experimental_rerun()
    if st.session_state.get('just_logged_out'):
        del st.session_state['just_logged_out']
        st.experimental_rerun()
    
    if not st.session_state['authenticated']:
        login()
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        if st.sidebar.button("Logout", key="logout_button"):
            logout()
        
        st.title("Crypto Token Analyzer")
        st.markdown("""
        Enter the name or symbol of a cryptocurrency token to analyze its scam likelihood.
        """)
        
        # Token input
        token_input = st.text_input("Enter Token Name or Symbol", value="", key="token_input")
        analyze_button = st.button("Analyze", key="analyze_button")
        
        # Sidebar settings
        st.sidebar.header("Trade Execution Bot Settings")
        
        enable_bot = st.sidebar.checkbox("Enable Trading Bot", value=False, key="enable_bot")
        scam_threshold = st.sidebar.slider("Scam Likelihood Threshold (%)", 0, 100, 20, key="scam_threshold")
        
        st.sidebar.markdown("""
        * **Enable Trading Bot:** Toggle to activate or deactivate the trading bot.
        * **Scam Likelihood Threshold:** Set the maximum scam likelihood percentage to consider a token safe for trading.
        """)
        
        if analyze_button and token_input:
            with st.spinner('Analyzing...'):
                analysis_result = analyze_token(token_input)
                display_results(analysis_result)
                
                scam_likelihood = extract_scam_likelihood(analysis_result)
                st.write(f"**Scam Likelihood:** {scam_likelihood}%")
                
                if enable_bot:
                    if scam_likelihood < scam_threshold:
                        st.success("Trading bot activated for this token.")
                        execute_trade(token_input)
                    else:
                        st.warning("Scam likelihood is above the threshold. Trading bot will not execute trades for this token.")

if __name__ == "__main__":
    main()
