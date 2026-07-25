import streamlit as st
from streamlit_gsheets import GSheetsConnection

# --- Set Background Color ---
background_color = "#d2fcfa"
label_text = "Masukkan Nombor Kad Pengenalan Graduan:"

# --- Single Combined CSS Block ---
st.markdown(
    f"""
    <style>
    /* Force main app viewport to flex correctly on mobile screens */
    html, body, .stApp {{
        height: 100%;
        min-height: -webkit-fill-available; /* Fixes iOS/Android dynamic address bar collapse */
        overflow-y: auto !important;
    }}

    div[data-testid="stAppViewContainer"] {{
        display: flex;
        flex-direction: column;
        flex: 1 1 auto;
        height: auto !important;
        min-height: 100%;
    }}

    div[data-testid="stMain"] {{
        flex: 1 1 auto;
    }}

    /* 1. Set app background color */
    .stApp {{
        background-color: {background_color};
    }}

    /* 2. Change text input label font size & weight */
    [data-testid="stWidgetLabel"] p, 
    [data-testid="stWidgetLabel"] span {{
        font-size: 26px !important;
        font-weight: regular !important;
    }}

    /* 3. Make button span full width */
    div[data-testid="stButton"] {{
        width: 100% !important;
    }}
    
    div[data-testid="stButton"] > button {{
        width: 100% !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(
    "SEMAKAN STATUS PENGAMBILAN JUBAH ISTIADAT KONVOKESYEN ADTEC JTM KALI KE-29"
)

# Establish connection to Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the sheet data (caches for 60s)
df = conn.read(ttl=60)

# Input field
user_id = st.text_input(label_text)

if st.button("Search", use_container_width=True):
    if user_id.strip():
        # Searches column named 'ID' (adjust column names to match your sheet)
        matches = df[df["ID"].astype(str).str.strip() == user_id.strip()]

        if not matches.empty:
            st.success("Record Found!")
            row = matches.iloc[0]

            st.write(f"**Name:** {row['NAMA']}")
            st.write(f"**Kampus:** {row['INSTITUT']}")
            st.write(f"**Kursus:** {row['KURSUS']}")
            st.write(f"**Saiz Jubah:** {row['SAIZ JUBAH']}")
            st.write(f"**Status:** {row['STATUS_JUBAH']}")
        else:
            st.error(f"No record found for ID: {user_id}")
    else:
        st.warning("Please enter an ID first.")
