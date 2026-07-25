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

# Read the sheet data (caches for 120s)
df = conn.read(ttl=120)

# --- ADD THE SANITIZATION CODE HERE ---
    # Replace 'IC_Nombor' with your actual column header name in Google Sheets
df['ID'] = (
    df['ID']
    .astype(str)
    .str.strip()
    .str.replace(r'\.0$', '', regex=True) # Removes .0 if pandas read it as float
    )
    # --------------------------------------

# Updated Input field with placeholder and help tooltip
user_id = st.text_input(
    label=label_text,
    placeholder="Contoh: 920101105123 atau 2026001",
    help="Masukkan nombor Kad Pengenalan atau ID tanpa sempang/ruang."
)

if st.button("Search", use_container_width=True):
    clean_user_input = user_id.strip().replace('.0', '')

    if clean_user_input:
        # 1. Clean the DataFrame column thoroughly
        cleaned_ids = (
            df["ID"]
            .astype(str)
            .str.strip()
            .str.replace(r'\.0$', '', regex=True) # Remove float decimal
        )

        # 2. Check for exact match OR match with padded leading zeros (e.g., 12 digits for IC)
        matches = df[
            (cleaned_ids == clean_user_input) | 
            (cleaned_ids == clean_user_input.zfill(12)) |
            (cleaned_ids.str.zfill(12) == clean_user_input)
        ]

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
