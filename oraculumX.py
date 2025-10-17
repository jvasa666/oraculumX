import os, random, time, requests
from io import BytesIO
import streamlit as st
import qrcode
from PIL import Image # Used by qrcode to create image objects

# ───────── CONFIG ─────────
ETH_ADDR = "0x5036dbcEEfae0a7429e64467222e1E259819c7C7"
# IMPORTANT: Replace with your actual BTC and Solana addresses if you want them to be real
BTC_ADDR = "bc1qzncgc94kgtcpumx80m5uedsp3hqp4fec2e3rvr" # Placeholder: Replace with your actual BTC address
SOL_ADDR = "7ckfzhhkwkpdTRHdXoEorD5gN3Yg6ggaTHw2B6gF6hKq" # Placeholder: Replace with your actual Solana address

THRESHOLD = 0.001  # ETH threshold to unlock premium
API_KEY = os.getenv("ETHERSCAN_API_KEY", "") # Ensure this environment variable is set for Etherscan API calls
REFRESH = 30  # seconds for auto-refresh
# ─────────────────────────

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="OraculumX • AI Crypto Signals",
    page_icon="🔮",
    layout="wide", # Use wide layout for the dashboard
    initial_sidebar_state="collapsed" # Collapsed by default as donations are in main content
)

# --- Custom CSS for Styling ---
st.markdown(
    """
    <style>
    /* General Streamlit container styling */
    .stApp {
        background-color: #1a1a2e; /* Dark blue/purple background */
        color: #e0e0e0; /* Light gray text */
        font-family: 'Arial', sans-serif;
    }

    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #e94560; /* Vibrant red/pink for headers */
        margin-top: 1.5em;
        margin-bottom: 0.8em;
    }
    h1 {
        text-align: center;
        font-size: 3em;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    }
    h2 {
        color: #00bcd4; /* Cyan for subheaders */
    }

    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 2.5em;
        color: #f0a500; /* Orange/gold for metrics */
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1em;
        color: #b0b0b0;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.9em;
        color: #28B463; /* Green for positive delta */
    }

    /* Buttons styling */
    .stButton button {
        background-color: #533483; /* Dark purple */
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
        margin: 5px; /* Add some margin around buttons */
        box-shadow: 3px 3px 8px rgba(0,0,0,0.4);
    }
    .stButton button:hover {
        background-color: #3e286e; /* Darker purple on hover */
        transform: scale(1.02);
    }
    .stButton button:active {
        transform: scale(0.98);
    }

    /* Style for the "Buy Me a Coffee" button specifically */
    .buy-me-a-coffee-button button {
        background-color: #FFDD00; /* Yellow for Ko-fi/BMC */
        color: #614B2A; /* Dark brown text */
        border: 2px solid #614B2A;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.4);
    }
    .buy-me-a-coffee-button button:hover {
        background-color: #E6C200;
        color: #614B2A;
    }

    /* General text styling for better readability */
    p {
        font-size: 1.1em;
        line-height: 1.6;
        color: #c0c0c0;
    }
    .section-header {
        font-size: 1.8em;
        font-weight: bold;
        color: #e94560; /* Vibrant red/pink */
        margin-top: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    .crypto-address {
        background-color: #2a2a4a; /* Darker background for code */
        padding: 8px;
        border-radius: 5px;
        font-family: monospace;
        word-break: break-all; /* Ensure long addresses wrap */
        white-space: pre-wrap; /* Preserve whitespace and wrap */
        font-size: 0.9em;
        color: #f0f0f0;
        border: 1px solid #3a3a5a;
    }
    .stInfo {
        background-color: #3a3a5a;
        color: #e0e0e0;
        border-left: 5px solid #00bcd4;
    }
    .stSuccess {
        background-color: #2a4a2a;
        color: #d0e0d0;
        border-left: 5px solid #28B463;
    }
    .stCodeBlock {
        background-color: #2a2a4a;
        color: #f0f0f0;
        border: 1px solid #3a3a5a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Function to generate QR code as a Streamlit image ---
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8, # Adjusted for main content
        border=4, # Adjusted for main content
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="transparent").convert('RGBA') # White QR, transparent background

    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# --- Main App Content ---
st.title("🔮 OraculumX – Future Signals from Beyond the Chain")
st.markdown("""
Welcome to **OraculumX**, your gateway to cutting-edge AI-driven crypto signals.
Our advanced algorithms analyze market trends to provide you with insights, helping you navigate the volatile crypto landscape.
""")

st.divider()

# Basic AI Alpha (Free)
st.subheader("🔥 Top 3 Coins to Watch (Free Tier)")
coins = ["GPT-AI", "SOL-Ape", "QuantumDOGE", "MemeGPT", "BASE-Warp", "ChainLINK", "ETH-Maxi"]
random.shuffle(coins) # Shuffle once at the beginning of the script run
for c in coins[:3]:
    st.write(f"• **{c}** – AI score: `{random.randint(75,99)}/100`")

st.divider()

# Tipping/Donation Panel
st.markdown('<p class="section-header">💎 Unlock Premium Signals & Support OraculumX</p>', unsafe_allow_html=True)
st.markdown(f"""
Your support helps us keep the lights on and continue developing advanced AI models.
**Send $\\geq$ `{THRESHOLD}` ETH to the address below to instantly unlock our Premium Alpha signals!**
""")

col_eth_qr, col_eth_details = st.columns([1, 2])

with col_eth_qr:
    st.image(generate_qr_code(ETH_ADDR), width=200, caption="Scan ETH for Premium Unlock")

with col_eth_details:
    st.markdown("### Ethereum (ETH) Address:")
    st.markdown(f'<div class="crypto-address">{ETH_ADDR}</div>', unsafe_allow_html=True)
    
    # Copy button logic
    if st.button("Copy ETH Address", key="copy_eth_main"):
        st.code(ETH_ADDR, language="text") # Display in a code block for easy copy
        st.success("ETH address copied to clipboard (see code block above)!")

    # MetaMask link
    st.markdown(f"""
    [Tap to tip via MetaMask](https://metamask.app.link/send/{ETH_ADDR})
    """)

# Optional: Check on-chain balance to unlock premium
def get_balance(addr):
    if not API_KEY:
        st.warning("Etherscan API Key not found. Premium unlock via ETH balance check is disabled.")
        return 0
    try:
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest&apikey={API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        if data["status"] == "1":
            wei = int(data["result"])
            return wei / 1e18
        else:
            st.error(f"Etherscan API error: {data.get('message', 'Unknown error')}")
            return 0
    except requests.exceptions.RequestException as e:
        st.error(f"Network error checking balance: {e}. Please check your internet connection or API key.")
        return 0
    except Exception as e:
        st.error(f"Error parsing Etherscan response: {e}")
        return 0

latest = get_balance(ETH_ADDR)
unlocked = latest >= THRESHOLD
status = "✅ Premium Unlocked! Enjoy the deep dive signals!" if unlocked else "🔒 Tip to Unlock Premium Signals"
st.info(status)

# Premium Alpha
if unlocked:
    st.header("🚀 Premium Alpha (AI Deep Dive)")
    st.markdown("""
    Welcome, Premium Member! Here are your exclusive, high-conviction signals.
    """)
    for c in coins[3:]: # Use the remaining coins from the shuffled list
        st.write(f"• **{c}** – Projection: `{random.randint(3,12)}x` in 48h")
else:
    st.caption("This panel auto-opens ~30s after your ETH payment hits the chain. Please wait for the page to refresh.")

st.divider()

# Additional Donation Options (Non-unlocking, just for general support)
st.markdown('<p class="section-header">💖 General Support & Community Links</p>', unsafe_allow_html=True)
st.markdown("""
If you wish to support OraculumX through other means, or just want to connect with our community,
we appreciate your generosity and engagement!
""")

col_bmc, col_social = st.columns(2)

with col_bmc:
    st.subheader("☕ Buy Me a Coffee")
    st.markdown("""
    A quick and easy way to show your appreciation!
    """)
    st.markdown(
        f"""
        <div class="buy-me-a-coffee-button">
            <a href="https://coff.ee/xenotech" target="_blank" style="text-decoration: none;">
                <button>
                    Buy Me a Coffee! ☕
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_social:
    st.subheader("🔗 Connect with Us")
    st.markdown("""
    Stay updated and join our growing community:
    """)
    st.markdown("""
    - 🌐 [Farcaster Profile](https://warpcast.com/xenotech)
    - 📢 [Telegram Channel](https://t.me/xenodrop)
    - 🔗 [Follow Lens](https://lens.xyz/u/xenotech)
    """)

st.divider()

# Other Crypto Donation Options (using expanders for tidiness)
st.subheader("Other Crypto Tip Addresses")
st.markdown("These addresses are for general tips and do not unlock premium features.")

col_btc, col_sol = st.columns(2)

with col_btc:
    with st.expander("Bitcoin (BTC)"):
        st.image(generate_qr_code(BTC_ADDR), width=150, caption="Scan BTC QR")
        st.markdown(f'<div class="crypto-address">{BTC_ADDR}</div>', unsafe_allow_html=True)
        if st.button("Copy BTC Address", key="copy_btc_other"):
            st.code(BTC_ADDR, language="text")
            st.success("BTC address copied to clipboard (see code block above)!")

with col_sol:
    with st.expander("Phantom/Solana (SOL)"):
        st.image(generate_qr_code(SOL_ADDR), width=150, caption="Scan SOL QR")
        st.markdown(f'<div class="crypto-address">{SOL_ADDR}</div>', unsafe_allow_html=True)
        if st.button("Copy SOL Address", key="copy_sol_other"):
            st.code(SOL_ADDR, language="text")
            st.success("SOL address copied to clipboard (see code block above)!")

st.markdown("---")
st.markdown("Thank you for being a part of the OraculumX journey!")

# Auto-refresh
time.sleep(REFRESH)
st.rerun()