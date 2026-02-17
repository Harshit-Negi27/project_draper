import streamlit as st
from src.graph import build_graph
# IMPORT THE HACKER SCRIPT
from twitter import post_tweet_visual_demo

# --- PAGE CONFIG ---
st.set_page_config(page_title="Project Draper", layout="wide")

st.title("🥃 Project Draper: Autonomous Marketing Agent")
st.markdown("Generates high-conversion content & **Deploys via Browser Agent**.")

# --- SESSION STATE INITIALIZATION ---
if "results" not in st.session_state:
    st.session_state.results = None
if "is_generated" not in st.session_state:
    st.session_state.is_generated = False

# --- SIDEBAR: INPUTS (CLEANED UP) ---
with st.sidebar:
    st.header("1. Campaign Details")
    product_name = st.text_input("Product Name", placeholder="e.g., OmniTask")
    product_url = st.text_input("Product URL (Optional)", placeholder="https://omnitask.com")
    product_desc = st.text_area("Brief Description", placeholder="What does it do? Who is it for?")
    
    st.divider()
    
    st.info("ℹ️ **Demo Mode:** Using Browser Automation Layer (Selenium) to bypass API costs.")
        
    generate_btn = st.button("Generate Campaign Strategy", type="primary")

# --- MAIN LOGIC ---

# 1. GENERATE CONTENT
if generate_btn and product_name:
    graph = build_graph()
    
    initial_state = {
        "product_name": product_name,
        "product_url": product_url,
        "product_description": product_desc,
        "research_data": "",
        "twitter_post": "",
        "linkedin_post": "",
        "facebook_post": "",
        "instagram_post": ""
    }
    
    with st.status("🤖 Draper is researching & drafting...", expanded=True) as status:
        st.write("🔍 Researching market & competitors...")
        # Run LangGraph
        st.session_state.results = graph.invoke(initial_state)
        st.session_state.is_generated = True
        status.update(label="Campaign Ready for Review", state="complete", expanded=False)

elif generate_btn and not product_name:
    st.error("Please enter a Product Name.")

# 2. DISPLAY & ACT (Only if content exists)
if st.session_state.is_generated and st.session_state.results:
    results = st.session_state.results
    
    st.divider()
    
    # --- TWITTER SECTION (THE STAR OF THE SHOW) ---
    st.subheader("🐦 Twitter / X Strategy")
    
    col_tweet, col_action = st.columns([3, 1])
    
    with col_tweet:
        # Editable Text Area
        tweet_content = st.text_area("Review Tweet", value=results.get("twitter_post"), height=150)
    
    with col_action:
        st.write("##") # Spacer
        
        # THE HACKER BUTTON
        if st.button("⚡ Execute Agent Action"):
            st.info("🔌 Handing over control to Browser Agent...")
            try:
                # Call the Selenium script
                post_tweet_visual_demo(tweet_content)
                st.success("✅ Posted successfully via Browser Automation!")
                st.balloons()
            except Exception as e:
                st.error(f"Agent Connection Failed: {e}")
                st.caption("Did you forget to launch the special Chrome window?")

    st.divider()
    
    # --- OTHER CHANNELS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📘 Facebook")
        st.info(results.get("facebook_post"))

    with col2:
        st.subheader("💼 LinkedIn")
        st.success(results.get("linkedin_post"))
        
        st.subheader("📸 Instagram Concept")
        st.warning(results.get("instagram_post"))
        
    with st.expander("See Research Data (Debug)"):
        st.json(results)