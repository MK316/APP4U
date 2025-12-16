
import streamlit as st

st.set_page_config(page_title="Final IPA Vowel Chart")

st.title("🌱 IPA English Consonant Chart")

tab1, tab2, tab3 = st.tabs(["English Consonants", "Allophones", "Diacritics"])

with tab1:
    st.markdown("Consonant chart")

with tab1:
    st.image("https://raw.githubusercontent.com/MK316/English-linguistics/main/pages/images/Cchart.png", caption="Consonant Chart", use_container_width=True)


with tab2:
    st.markdown("To be updated.")


with tab3:
    st.markdown("📌 To be updated.")
