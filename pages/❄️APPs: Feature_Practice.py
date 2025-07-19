import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import random

tab1, tab2, tab3, tab4 = st.tabs(["🌀 Feature matrix for consonants","🌀 Practice Applications","🌀 Vowel features","🌀 Natural class"])

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

# Grouped features based on previous dictionary
grouped_features = {
    '[+voice]': ['b', 'd', 'g', 'dʒ', 'v', 'ð', 'z', 'ʒ', 'm', 'n', 'ŋ', 'l', 'r', 'j', 'w'],
    '[-voice]': ['p', 't', 'k', 'tʃ', 'f', 'θ', 's', 'ʃ', 'h'],
    '[+anterior]': ['p', 'b', 't', 'd', 'f', 'v', 'θ', 'ð', 's', 'z', 'm', 'n', 'l', 'r'],
    '[+coronal]': ['t', 'd', 'tʃ', 'dʒ', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'n', 'l', 'r'],
    '[+delayed release]': ['tʃ', 'dʒ'],
    '[+sonorant]': ['m', 'n', 'ŋ', 'l', 'r', 'j', 'w'],
    '[+strident]': ['tʃ', 'dʒ', 'f', 'v', 's', 'z', 'ʃ', 'ʒ'],
    '[+nasal]': ['m', 'n', 'ŋ'],
    '[+continuant]': ['f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'h', 'l', 'r', 'j', 'w'],
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
        df = pd.DataFrame(vowel_features)  # Transpose to make symbols columns and features rows
        return df
    
    def app():
        st.markdown('#### 🐣 Vowel Feature Matrix')
        st.write('This matrix displays the distinctive features for English vowels in IPA.')

        # Generate the feature matrix DataFrame
        feature_matrix = create_feature_matrix(vowel_features)
    
        # Display the feature matrix
        st.dataframe(feature_matrix, height=260, use_container_width=True)

        st.info("Note 1: The vowel [ʌ] is phonologically marked as [+back], even though it is phonetically pronounced more centrally. This distinction may not be crucial for the TCE exam.")
        
        st.info("Note 2: The vowel [ɔ] is marked as [+tense] here. You may encounter different descriptions in various textbooks.")

    if __name__ == "__main__":
        app()




# Function to generate question sets
def generate_questions(num_sets):
    questions = []
    for _ in range(num_sets):
        feature, sounds = random.choice(list(grouped_features.items()))
        if len(sounds) > 5:
            sound_group = random.sample(sounds, 5)
        else:
            sound_group = sounds
        questions.append((sound_group, feature))
    return questions
    
with tab4:
    with st.expander("**Instructions**"):
        st.info("""
        **Consider the following features only:**  
        [+voice], [-voice], [+anterior], [+coronal], [+delayed release],  
        [+sonorant], [+strident], [+nasal], [+continuant]  
        Write answers in square brackets, like `[+voice]` or `[+nasal]`.
        """)
    
    # Initialize session state
    if 'questions' not in st.session_state:
        st.session_state['questions'] = []
    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = 0
    if 'score' not in st.session_state:
        st.session_state['score'] = 0
    if 'answered' not in st.session_state:
        st.session_state['answered'] = False
    
    # Step 1: Ask the user how many sets they want to practice
    if not st.session_state['questions']:
        num_sets = st.number_input("How many sets would you like to practice?", min_value=1, max_value=10, value=5)
        if st.button("Start Practice"):
            st.session_state['questions'] = generate_questions(num_sets)
            st.session_state['current_question'] = 0
            st.session_state['score'] = 0
            st.session_state['answered'] = False
            st.rerun()
    
    # Step 2: Display the question
    if st.session_state['questions']:
        current_set = st.session_state['questions'][st.session_state['current_question']]
        sounds, correct_answer = current_set
        
        st.markdown(f"### **Identify the Common Feature**")
        st.write(f"**Sounds:** [{', '.join(sounds)}]")
    
        # Step 3: Ask the user for input
        st.write("Which feature is shared among these sounds?")
        user_answer = st.text_input("Write feature with value (e.g., [+voice], [-nasal]):", value="")
    
        # Step 4: Check answer and give feedback
        if st.button("Check Answer"):
            # Clean user answer and correct answer formatting
            cleaned_user_answer = user_answer.strip().replace(" ", "")
            cleaned_correct_answers = [ans.strip().replace(" ", "") for ans in correct_answer.split(",")]
    
            # Ensure all correct answers have square brackets
            cleaned_correct_answers = [
                f"[{ans}]" if not ans.startswith("[") else ans for ans in cleaned_correct_answers
            ]
    
            # Allow space variation and ensure both answers are in square brackets
            if cleaned_user_answer in cleaned_correct_answers:
                st.session_state['score'] += 1
                st.success(f"✅ Correct! The shared feature is **{cleaned_user_answer}**.")
            else:
                st.error(f"❌ Incorrect. The correct answer(s) are: {', '.join(cleaned_correct_answers)}")
    
            st.session_state['answered'] = True
    
        # Step 5: Next question button
        if st.session_state['answered']:
            if st.session_state['current_question'] < len(st.session_state['questions']) - 1:
                if st.button("Next Question"):
                    st.session_state['current_question'] += 1
                    st.session_state['answered'] = False
                    st.rerun()
            else:
                st.write("✅ **Practice Completed!**")
                st.write(f"**Your score: {st.session_state['score']}/{len(st.session_state['questions'])}**")
                if st.button("Restart Practice"):
                    st.session_state['questions'] = []
                    st.session_state['current_question'] = 0
                    st.session_state['score'] = 0
                    st.session_state['answered'] = False
                    st.rerun()
