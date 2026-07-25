import streamlit as st
from streamlit_gsheets import GSheetsConnection

# --- Set Background Color ---
# Replace #f0f2f6 with any hex color, CSS color name, or RGB value you prefer
background_color = "#d2fcfa"
label_text = "Masukkan Nombor Kad Pengenalan Graduan:"

st.markdown(
    f"""
    <style>
    /* Change background for the main content area */
    .stApp {{
        background-color: {background_color};
    }}

    /* 2. Change text input label font size */
    div[data-testid="stWidgetLabel"] p {{
        font-size: 22px !important;
        font-weight: bold !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("SEMAKAN STATUS PENGAMBILAN JUBAH ISTIADAT KONVOKESYEN ADTEC JTM KALI KE-29")

# Establish connection to Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the sheet data (caches for 60s)
df = conn.read(ttl=60)

# Input field
user_id = st.text_input("Masukkan Nombor Kad Pengenalan Graduan:")

if st.button("Search"):
    if user_id.strip():
        # Searches column named 'ID' (adjust column names to match your sheet)
        matches = df[df['ID'].astype(str).str.strip() == user_id.strip()]
        
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
