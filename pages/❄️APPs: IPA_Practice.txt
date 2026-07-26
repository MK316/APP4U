import streamlit as st

def phonetics_apps_page():
    st.title('🐾 [fəˈnɛɾɪks] Apps')
    st.write('Applications used to teach Phonetics.')

    # Describing your apps briefly
    st.markdown("""
    Here is a selection of applications designed to enhance phonetics learning through interactive and innovative tools. These apps provide resources and exercises to improve pronunciation, listening skills, and phonetic awareness.
    """)

    # First row with three columns
    col1, col2, col3 = st.columns(3)  # Define columns for the first row

    with col1:
        st.image("images/button01.png", width=100)
        if st.button('App 1: \nIPA practice', key='1'):
            st.markdown("🌀[App link](https://ipa-practice.streamlit.app/): IPA Quiz with phonetic descriptions; Scoring", unsafe_allow_html=True)
            st.markdown("[Report](https://padlet.com/mirankim316/ipa) your record!")
            st.markdown("[Ranking](https://ipa-ranking.streamlit.app/)")
            st.markdown("2024.10.14")
    with col2:
        st.image("images/button01.png", width=100)
        if st.button('App 2: IPA quiz', key='2'):
            st.markdown("🌀[App link](https://ipa-quiz2.streamlit.app/): Individual sound description quiz", unsafe_allow_html=True)
            st.caption("24 consonants and 11 vowel symbols")
            st.markdown("2024.10.20")

    with col3:
        st.image("images/button01.png", width=100)
        if st.button('App 4: List sounds', key='4'):
            st.markdown("🌀[App link](https://mk-316-ipaselect.hf.space/): Display sounds from phonetic descriptions", unsafe_allow_html=True)
            st.markdown("2024.10.14")


phonetics_apps_page()

# URL to the raw image on GitHub
image_url = "https://github.com/MK316/MK-316/raw/main/images/bg2.png"
# Display the image
st.image(image_url, caption="\"He who knows no foreign languages knows nothing of his own.\" — Johann Wolfgang von Goethe", use_container_width=True)
