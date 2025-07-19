import streamlit as st
import random

# IPA Data from your original dictionary
ipa_data = {
    'p': {'Voicing': 'voiceless', 'Place': 'bilabial', 'Manner': 'stop','Oro-nasal': '(oral)','Centrality':'(central)'},
    'b': {'Voicing': 'voiced', 'Place': 'bilabial', 'Manner': 'stop','Oro-nasal': '(oral)','Centrality':'(central)'},
    't': {'Voicing': 'voiceless', 'Place': 'alveolar', 'Manner': 'stop','Oro-nasal': '(oral)','Centrality':'(central)'},
    'd': {'Voicing': 'voiced', 'Place': 'alveolar', 'Manner': 'stop','Oro-nasal': '(oral)','Centrality':'(central)'},
    'k': {'Voicing': 'voiceless', 'Place': 'velar', 'Manner': 'stop','Oro-nasal': '(oral)','Centrality':'(central)'},
    'g': {'Voicing': 'voiced', 'Place': 'velar', 'Manner': 'stop','Oro-nasal': '(oral)','Centrality':'(central)'},
    'f': {'Voicing': 'voiceless', 'Place': 'labio-dental', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'v': {'Voicing': 'voiced', 'Place': 'labio-dental', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'θ': {'Voicing': 'voiceless', 'Place': 'dental', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'ð': {'Voicing': 'voiced', 'Place': 'dental', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    's': {'Voicing': 'voiceless', 'Place': 'alveolar', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'z': {'Voicing': 'voiced', 'Place': 'alveolar', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'ʃ': {'Voicing': 'voiceless', 'Place': 'palato-alveolar', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'ʒ': {'Voicing': 'voiced', 'Place': 'palato-alveolar', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'tʃ': {'Voicing': 'voiceless', 'Place': 'palato-alveolar', 'Manner': 'affricate','Oro-nasal': '(oral)','Centrality':'(central)'},
    'dʒ': {'Voicing': 'voiced', 'Place': 'palato-alveolar', 'Manner': 'affricate','Oro-nasal': '(oral)','Centrality':'(central)'},
    'h': {'Voicing': 'voiceless', 'Place': 'glottal', 'Manner': 'fricative','Oro-nasal': '(oral)','Centrality':'(central)'},
    'm': {'Voicing': 'voiced', 'Place': 'bilabial', 'Manner': 'stop','Oro-nasal': 'nasal','Centrality':'(not applicable)'},
    'n': {'Voicing': 'voiced', 'Place': 'alveolar', 'Manner': 'stop','Oro-nasal': 'nasal','Centrality':'(not applicable)'},
    'ŋ': {'Voicing': 'voiced', 'Place': 'velar', 'Manner': 'stop','Oro-nasal': 'nasal','Centrality':'(not applicable)'},
    'ɹ': {'Voicing': 'voiced', 'Place': 'alveolar', 'Manner': 'approximant','Oro-nasal': '(oral)','Centrality':'(central)'},
    'l': {'Voicing': 'voiced', 'Place': 'alveolar', 'Manner': 'approximant','Oro-nasal': '(oral)','Centrality':'lateral'},
    'j': {'Voicing': 'voiced', 'Place': 'palatal', 'Manner': 'approximant','Oro-nasal': '(oral)','Centrality':'(central)'},
    'w': {'Voicing': 'voiced', 'Place': 'labio-velar', 'Manner': 'approximant','Oro-nasal': '(oral)','Centrality':'(central)'}
}


def select_random_symbol():
    """Select a random IPA symbol"""
    symbol = random.choice(list(ipa_data.keys()))
    return symbol, ipa_data[symbol]

def validate_selections(ipa_symbol, user_voicing, user_place, user_manner, user_oronasal, user_centrality):
    """Check user's selections against the actual IPA symbol properties"""
    correct_data = ipa_data[ipa_symbol]
    correct = (correct_data['Voicing'] == user_voicing and
               correct_data['Place'] == user_place and
               correct_data['Manner'] == user_manner and
               correct_data['Oro-nasal'] == user_oronasal and
               correct_data['Centrality'] == user_centrality)
    
    return correct, correct_data

# Main interface with Streamlit
st.title("💧 IPA Practice App")

# Textbox for user name input, always available
user_name = st.text_input("Enter your name:", value=st.session_state.user_name if 'user_name' in st.session_state else "")

# Start quiz button
if st.button("Start Quiz"):
    st.session_state.user_name = user_name
    st.session_state.correct_count = 0
    st.session_state.attempts = 0
    st.session_state.current_symbol, st.session_state.current_data = select_random_symbol()

if "current_symbol" in st.session_state:
    st.write(f"IPA Symbol: {st.session_state.current_symbol}")
    st.markdown("📌 Note: Liquids and glides are approximants.")
    st.info("For the centrality of a sound, mark 'Not applicable' when the air goes through the nose.")
    # Using columns to organize the options
    col1, col2, col3, col4, col5 = st.columns([1.7, 2.3, 2.2, 1.5, 2.3])
    with col1:
        voicing = st.radio("Voicing", ['voiceless', 'voiced'], key=f"voicing_{st.session_state.attempts}")
    with col2:
        place = st.radio("Place", ['bilabial', 'labio-dental', 'labio-velar', 'dental', 'alveolar', 'palato-alveolar', 'palatal', 'velar', 'glottal'], key=f"place_{st.session_state.attempts}")
    with col3:
        manner = st.radio("Manner", ['stop', 'fricative', 'affricate', 'approximant'], key=f"manner_{st.session_state.attempts}")
    with col4:
        oronasal = st.radio("Oro-nasal", ['(oral)', 'nasal'], key=f"oronasal_{st.session_state.attempts}")
    with col5:
        centrality = st.radio("Centrality", ['(central)', 'lateral', '(not applicable)'], key=f"centrality_{st.session_state.attempts}")

    # Place buttons next to each other without any gap
    cols = st.columns([2, 3, 5])  # Adjust the width of the first two columns to bring buttons closer
    with cols[0]:
        submit_pressed = st.button("Submit")
    with cols[1]:
        continue_pressed = st.button("Show score & Continue")

    # Process the submission and update
    if submit_pressed:
        correct, _ = validate_selections(st.session_state.current_symbol, voicing, place, manner, oronasal, centrality)
        if correct:
            st.success("Correct!")
            st.session_state.correct_count += 1
        else:
            st.error("Incorrect!")
        st.session_state.attempts += 1
        st.session_state.current_symbol, st.session_state.current_data = select_random_symbol()

    # Show score when 'Continue' is pressed
    if continue_pressed:
        st.write(f"{st.session_state.user_name if 'user_name' in st.session_state else 'User'} score: {st.session_state.correct_count} out of {st.session_state.attempts}")
