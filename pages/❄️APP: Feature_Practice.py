import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

tab1, tab2, tab3 = st.tabs(["🌀 Feature matrix for consonants","🌀 Practice Applications","🌀 Vowel features"])

# IPA features dictionary with full feature names
ipa_features = {
    'p': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'b': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    't': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'd': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'k': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'g': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'tʃ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '+', 'voice': '-'},
    'dʒ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '-', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '+', 'voice': '+'},
    'f': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'v': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'θ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'ð': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    's': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'z': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'ʃ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'ʒ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '+', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '+', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'h': {'syllabic': '-', 'consonantal': '+', 'sonorant': '-', 'coronal': '-', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '-'},
    'm': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '-', 'anterior': '+', 'continuant': '-', 'nasal': '+', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'n': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '+', 'anterior': '+', 'continuant': '-', 'nasal': '+', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'ŋ': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '-', 'anterior': '-', 'continuant': '-', 'nasal': '+', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'l': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '+', 'delayed release': '-', 'voice': '+'},
    'r': {'syllabic': '-', 'consonantal': '+', 'sonorant': '+', 'coronal': '+', 'anterior': '+', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'j': {'syllabic': '-', 'consonantal': '-', 'sonorant': '+', 'coronal': '-', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'},
    'w': {'syllabic': '-', 'consonantal': '-', 'sonorant': '+', 'coronal': '-', 'anterior': '-', 'continuant': '+', 'nasal': '-', 'strident': '-', 'lateral': '-', 'delayed release': '-', 'voice': '+'}
}

# Define vowel features
vowel_features = {
    '[i]': {'[high]': '+', '[low]': '-', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '+'},
    '[ɪ]': {'[high]': '+', '[low]': '-', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[ɛ]': {'[high]': '-', '[low]': '-', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[æ]': {'[high]': '-', '[low]': '+', '[front]': '+', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[ə]': {'[high]': '-', '[low]': '-', '[front]': '-', '[back]': '-', '[rounded]': '-', '[tense]': '-'},
    '[u]': {'[high]': '+', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '+', '[tense]': '+'},
    '[ʊ]': {'[high]': '+', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '+', '[tense]': '-'},
    '[ʌ]': {'[high]': '-', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '-', '[tense]': '-'},
    '[ɔ]': {'[high]': '-', '[low]': '-', '[front]': '-', '[back]': '+', '[rounded]': '+', '[tense]': '+'},
    '[ɑ]': {'[high]': '-', '[low]': '+', '[front]': '-', '[back]': '+', '[rounded]': '-', '[tense]': '+'}
}

# Dictionary comprehension to modify keys to include brackets
modified_ipa_features = {phoneme: {'[' + feature + ']': value for feature, value in features.items()} for phoneme, features in ipa_features.items()}

# Now modified_ipa_features contains the updated keys
# print(modified_ipa_features)

with tab1:
    def create_feature_matrix(ipa_features):
        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(ipa_features)  # Transpose to make symbols columns and features rows
        return df
    
    def app():
        st.markdown('#### 🐣 Consonant Feature Matrix')
        st.write('This matrix displays the distinctive features for 24 English consonants in IPA.')
    
        # Generate the feature matrix DataFrame
        feature_matrix = create_feature_matrix(modified_ipa_features)
    
        # Display the feature matrix
        st.dataframe(feature_matrix, height=440, use_container_width=True)
    
    if __name__ == "__main__":
        app()

with tab2:
    st.markdown('### 🐾 Distinctive Feature Practice Apps')
    st.write('Applications to train yourself with distinctive features in phonology')

    # Describing your apps briefly
    st.caption("""
    Here is a selection of applications designed to enhance feature matrix learning through interactive and innovative tools.
    """)

    # First row with three columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("images/button01.png", width=100)
        if st.button('App 1: Distinctive features', key='3'):
            st.markdown("🌀 [App link](https://mk-316-featureapp01.hf.space/): Basic level - Sound lists by feature marking ")
            st.markdown("Updated on: 2024.10.15")
    with col2:
        st.image("images/button01.png", width=100)
        if st.button('App 2: Feature Quiz 1', key='5'):
            st.markdown("🌀 [App link](https://mk-316-feature-practice.hf.space/): Basic level - Feature marking for individual segments")
            st.markdown("Updated on: 2024.10.14")
    with col3:
        st.image("images/button01.png", width=100)
        if st.button('App 3: Feature Quiz 2', key='6'):
            st.markdown("🌀 [App link](https://feature-quiz02.streamlit.app/): Level 1 - Distinctive feature quiz (choose)")
            st.markdown("Updated on: 2024.11.6")

    # URL to the raw image on GitHub
    image_url = "https://github.com/MK316/MK-316/raw/main/images/bg2.png"
    # Display the image
    st.image(image_url, caption="\"He who knows no foreign languages knows nothing of his own.\" — Johann Wolfgang von Goethe", use_container_width=True)

with tab3: 
    def create_feature_matrix(vowel_features):
        # Convert the dictionary to a DataFrame and transpose it
        df = pd.DataFrame(vowel_features).T  # Transpose to make symbols columns and features rows
        return df
    
    def app():
        st.markdown('#### 🐣 Vowel Feature Matrix')
        st.write('This matrix displays the distinctive features for English vowels in IPA.')
        st.info("Note 1: [ʌ] is phonologically marked as [+back] even though it is phonetically pronounced as central. This may not be so important for TCE exam.")
        st.info("Note 2: [ɔ] is marked as [+tense] here. You may find different descriptions depending on textbooks.")
        # Generate the feature matrix DataFrame
        feature_matrix = create_feature_matrix(vowel_features)
    
        # Display the feature matrix
        st.dataframe(feature_matrix, height=440, use_container_width=True)
    
    if __name__ == "__main__":
        app()
