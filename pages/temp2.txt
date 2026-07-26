import streamlit as st
import pandas as pd
from gtts import gTTS
import io

st.set_page_config(page_title="Classroom English Trainer", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/1Oa8RtJ8P1KuRTWafcGxXTWTQ83KuKBWx466-jrq1Aig/export?format=csv&gid=0"


@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

def tts_bytes(text: str, lang: str = "en"):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

df = load_data()

st.title("Classroom English Streamlit App 🎓")

tab1, tab2, tab3 = st.tabs(
    ["Classroom English Practice", "Tab 2 (Coming Soon)", "Tab 3 (Coming Soon)"]
)

with tab1:
    st.header("English Expressions for EFL Classrooms")

    categories = df["category"].unique()
    category = st.selectbox("Choose a classroom situation:", categories)

    subset = df[df["category"] == category].sort_values("script_id")

    for _, row in subset.iterrows():
        label = f"{row['category']} – Script {row['script_id']}"
        with st.expander(label):
            st.write(row["text"])
            if st.button(f"▶️ Play audio for Script {row['script_id']}", key=f"{row['category']}_{row['script_id']}"):
                audio_data = tts_bytes(row["text"])
                st.audio(audio_data, format="audio/mp3")


with tab2:
    st.header("Tab 2")
    st.write("This tab is reserved for future activities (e.g., role-plays, quizzes, or recording practice).")

with tab3:
    st.header("Tab 3")
    st.write("This tab is reserved for future expansions, such as saving favorite expressions or creating custom scripts.")
