import streamlit as st
import requests
from datetime import datetime

API_KEY = '7611414363:AAFjNyVPsgfE7hfODHOP9hyhLbvNPSx5Fzg'
CHATID = '362032442'
# Set page config
st.set_page_config(layout="wide")
st.title("Selora Bot cPanel")
# Hardcoded Telegram credentials
BOT_TOKEN = API_KEY  # Replace with your bot token
CHAT_ID = CHATID      # Replace with your chat ID

# Function to send message to Telegram
def send_to_telegram(message_text):
    try:
        send_message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        # Prepare the message
        formatted_message = f"""
🤖 New Command Received:
📊 Data:
{message_text}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Send the message
        response = requests.post(
            send_message_url,
            json={
                "chat_id": CHAT_ID,
                "text": formatted_message,
                "parse_mode": "HTML"
            }
        )
        
        if response.status_code == 200:
            return True, "Message sent successfully to Telegram!"
        else:
            return False, f"Failed to send message: {response.text}"
            
    except Exception as e:
        return False, f"Error sending message: {str(e)}"

# [Rest of your existing code...]
st.markdown("""
    <style>
    .tooltip-container {
        position: relative;
        display: inline-flex;
        align-items: center;
    }
    
    .tooltip-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background-color: #f0f2f6;
        color: #0f1215;
        font-size: 12px;
        font-weight: bold;
        margin-left: 5px;
        cursor: help;
    }
    
    .tooltip-content {
        visibility: hidden;
        position: absolute;
        z-index: 1000;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 14px;
        width: max-content;
        max-width: 200px;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        margin-top: 5px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    /* Arrow for tooltip */
    .tooltip-content::after {
        content: "";
        position: absolute;
        bottom: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: transparent transparent #333 transparent;
    }
    
    .tooltip-container:hover .tooltip-content {
        visibility: visible;
        opacity: 1;
    }
    
    .tooltip-icon:hover {
        background-color: #e1e4e8;
    }
    </style>
""", unsafe_allow_html=True)

def add_tooltip(label, tooltip_text):
    return f"""
        <div class="tooltip-container">
            {label}
            <div class="tooltip-icon">?
                <span class="tooltip-content">{tooltip_text}</span>
            </div>
        </div>
    """

# Center the circular image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <style>
        .circular-image {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            object-fit: cover;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<img src="https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg?t=st=1731837470~exp=1731841070~hmac=5a71bce31926e1791d72ea924c759dccd61d8d7fd369e7bf1224693738e3ed48&w=1480" class="circular-image">',
        unsafe_allow_html=True
    )

st.markdown("---")

# Sell Threshold percentage input with tooltip
st.markdown(add_tooltip(
    "Sell Threshold %",
    "Set the percentage threshold at which the system will trigger a sell order"
), unsafe_allow_html=True)
sell_threshold = st.number_input(
    "",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.1f"
)

st.markdown("---")

# Create two columns for the number inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown(add_tooltip(
        "Maximum Limit",
        "The maximum amount that can be processed in a single transaction"
    ), unsafe_allow_html=True)
    max_limit = st.number_input(
        "",
        min_value=0,
        max_value=1000000,
        value=1000,
        step=100
    )

with col2:
    st.markdown(add_tooltip(
        "Confirmation Code",
        "Enter your security code to confirm changes"
    ), unsafe_allow_html=True)
    confirmation_code = st.text_input(
        "",
        type="password"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Create three columns to center the button
button_col1, button_col2, button_col3 = st.columns([2, 1, 2])

with button_col2:
    if st.button("Send Command", type="primary", use_container_width=True):
        if not confirmation_code:
            st.error("Please enter a confirmation code")
        else:
            # Prepare the data
            settings = {
                "sell_threshold": f"{sell_threshold}%",
                "maximum_limit": max_limit,
                "confirmation_code": "****"
            }
            
            # Send to Telegram
            success, message = send_to_telegram(str(settings))
            
            if success:
                st.success("Settings updated and sent to Telegram successfully!")
                st.write("Sent values:", settings)
            else:
                st.error(f"Error sending to Telegram: {message}")