import streamlit as st
import random
import re

# ---- Score display

# Initialize per-session score tracking
if "tab2_score" not in st.session_state:
    st.session_state.tab2_score = 0
if "tab2_total" not in st.session_state:
    st.session_state.tab2_total = 0
if "tab3_score" not in st.session_state:
    st.session_state.tab3_score = 0
if "tab3_total" not in st.session_state:
    st.session_state.tab3_total = 0



# --- IPA Consonant Dictionary ---
consonants = [
    {"symbol": "p", "voicing": "voiceless", "place": "bilabial", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "b", "voicing": "voiced", "place": "bilabial", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "t", "voicing": "voiceless", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "d", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "k", "voicing": "voiceless", "place": "velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "g", "voicing": "voiced", "place": "velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "plosive"},
    {"symbol": "f", "voicing": "voiceless", "place": "labiodental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "v", "voicing": "voiced", "place": "labiodental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "θ", "voicing": "voiceless", "place": "dental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "ð", "voicing": "voiced", "place": "dental", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "s", "voicing": "voiceless", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "z", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "ʃ", "voicing": "voiceless", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "ʒ", "voicing": "voiced", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "h", "voicing": "voiceless", "place": "glottal", "oro_nasal": "oral", "centrality": "(central)", "manner": "fricative"},
    {"symbol": "tʃ", "voicing": "voiceless", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "affricate"},
    {"symbol": "dʒ", "voicing": "voiced", "place": "post-alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "affricate"},
    {"symbol": "m", "voicing": "voiced", "place": "bilabial", "oro_nasal": "nasal", "centrality": "(central)", "manner": "nasal"},
    {"symbol": "n", "voicing": "voiced", "place": "alveolar", "oro_nasal": "nasal", "centrality": "(central)", "manner": "nasal"},
    {"symbol": "ŋ", "voicing": "voiced", "place": "velar", "oro_nasal": "nasal", "centrality": "(central)", "manner": "nasal"},
    {"symbol": "l", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "lateral", "manner": "approximant "},
    {"symbol": "ɹ", "voicing": "voiced", "place": "alveolar", "oro_nasal": "oral", "centrality": "(central)", "manner": "approximant"},
    {"symbol": "j", "voicing": "voiced", "place": "palatal", "oro_nasal": "oral", "centrality": "(central)", "manner": "glide"},
    {"symbol": "w", "voicing": "voiced", "place": "labio-velar", "oro_nasal": "oral", "centrality": "(central)", "manner": "glide"},
]

def display_score(tab_label):
    score = st.session_state[f"{tab_label}_score"]
    total = st.session_state[f"{tab_label}_total"]
    st.markdown(f"**Score: {score} / {total}**")


# --- UI Layout ---
tab1, tab2, tab3 = st.tabs(["[1] Explore Sounds", "[2] Identify Symbol", "[3] Identify Key Difference"])

# ----------------- TAB 1 -----------------
with tab1:
    st.header("🔎 IPA Sound Filter")

    voicing = st.selectbox("[1] Voicing (VD vs. VL)", ["Any", "voiced", "voiceless"])
    place = st.selectbox("[2] Place of articulation", ["Any", "bilabial", "labiodental", "dental", "alveolar", "post-alveolar", "palatal", "labio-velar", "velar", "glottal"])
    oro_nasal = st.selectbox("[3] Oro-nasal process (Oral vs. Nasal)", ["Any", "oral", "nasal"])
    centrality = st.selectbox("[4] Centrality (Central vs. Lateral)", ["Any", "(central)", "lateral"])
    manner = st.selectbox("[5] Manner of articulation", ["Any", "plosive", "nasal", "fricative", "affricate", "approximant (lateral)", "approximant (non-lateral)", "glide"])

    # Define place articulation order
    place_order = {
        "bilabial": 1,
        "labiodental": 2,
        "dental": 3,
        "alveolar": 4,
        "post-alveolar": 5,
        "palatal": 6,
        "labio-velar": 7,
        "velar": 8,
        "glottal": 9
    }

    # Filter consonants
    filtered = [
        c for c in consonants
        if (voicing == "Any" or c["voicing"] == voicing)
        and (place == "Any" or c["place"] == place)
        and (oro_nasal == "Any" or c["oro_nasal"] == oro_nasal)
        and (centrality == "Any" or c["centrality"] == centrality)
        and (manner == "Any" or c["manner"] == manner)
    ]

    # Sort by place of articulation
    filtered.sort(key=lambda c: place_order.get(c["place"], 99))

    st.markdown(f"### 🎯 {len(filtered)} result(s):")

    if filtered:
        # Sort by place of articulation (following typical order)
        place_order = [
            "bilabial", "labiodental", "dental", "alveolar",
            "post-alveolar", "palatal", "labio-velar", "velar", "glottal"
        ]

        place_groups = {}
        for c in filtered:
            place = c["place"]
            if place not in place_groups:
                place_groups[place] = []
            place_groups[place].append(c["symbol"])

        # Display grouped sounds by place in the defined order
        for place in place_order:
            if place in place_groups:
                symbols = ", ".join([f"<span style='font-size:1.6em'>{s}</span>" for s in place_groups[place]])
                st.markdown(f"{symbols} <span style='color:gray'>({place})</span><br>", unsafe_allow_html=True)
    else:
        st.info("No matching sounds found.")




# ----------------- TAB 2 -----------------
with tab2:

    st.header("🌳 Identify the Correct IPA Symbol")

    display_score("tab2")

    # Initialize session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "options" not in st.session_state:
        st.session_state.options = []
    if "answer" not in st.session_state:
        st.session_state.answer = None

    def new_question():
        st.session_state.current_question = random.choice(consonants)
        correct = st.session_state.current_question
        distractors = random.sample([c for c in consonants if c != correct], 4)
        options = distractors + [correct]
        random.shuffle(options)
        st.session_state.options = options
        st.session_state.answer = correct['symbol']

    # Trigger new question at start or after "Next"
    if st.session_state.current_question is None:
        new_question()

    question = st.session_state.current_question

    if question:
        # Format manner
        if question["manner"] == "nasal":
            desc = f"{question['place']} ({question['oro_nasal']}) nasal (stop)"
        else:
            manner_display = question["manner"]
            # Drop centrality if manner includes 'lateral'
            centrality_display = "" if "lateral" in manner_display else question["centrality"]
            desc_parts = [
                question["voicing"],
                question["place"],
                f"({question['oro_nasal']})",
                centrality_display,
                manner_display
            ]
            desc = " ".join([part for part in desc_parts if part])

        # Style bracketed text gray
        desc_html = re.sub(r"\((.*?)\)", r"<span style='color:gray'>(\1)</span>", desc)
        st.markdown(f"#### Which symbol matches: *{desc_html}*?", unsafe_allow_html=True)

        # Show options
        choice = st.radio("Choose one:", [c['symbol'] for c in st.session_state.options], key="tab2_choice_radio")

        # Buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("Check answer", key="tab2_check_btn"):
                st.session_state.tab2_total += 1
                if choice == st.session_state.answer:
                    st.session_state.tab2_score += 1
                    st.success("✅ Correct!")
                else:
                    st.error("❌ Try again.")

                # 🎉 Trigger balloons if user reaches 20/20
                if st.session_state.tab2_score == 20 and st.session_state.tab2_total == 20:
                    st.balloons()

        with col2:
            if st.button("Next", key="tab2_next_btn"):
                new_question()
                st.rerun()

        with col3:
            if st.button("🔁 Reset Session", key="tab2_reset_btn"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()



# ----------------- TAB 3 -----------------
with tab3:
    st.header("🧩 Find the Key Feature Difference(s)")

    display_score("tab3")

    # Fixed options for difference types
    diff_options = [
        "Voicing",
        "Place",
        "Oro-nasal process (oral vs. nasal)",
        "Centrality (central vs. lateral)",
        "Manner"
    ]

    def get_key_differences(c1, c2):
        """Return a list of ALL features that differ between c1 and c2."""
        diffs = []
        if c1["voicing"] != c2["voicing"]:
            diffs.append("Voicing")
        if c1["place"] != c2["place"]:
            diffs.append("Place")
        if c1["oro_nasal"] != c2["oro_nasal"]:
            diffs.append("Oro-nasal process (oral vs. nasal)")
        if c1["centrality"] != c2["centrality"]:
            diffs.append("Centrality (central vs. lateral)")
        if c1["manner"] != c2["manner"]:
            diffs.append("Manner")
        return diffs

    def new_pair():
        while True:
            c1, c2 = random.sample(consonants, 2)
            diffs = get_key_differences(c1, c2)
            if diffs:
                st.session_state.pair = (c1, c2)
                st.session_state.key_diffs = diffs
                st.session_state.tab3_round = st.session_state.get("tab3_round", 0) + 1
                break

    if "pair" not in st.session_state or "key_diffs" not in st.session_state:
        new_pair()
    if "tab3_round" not in st.session_state:
        st.session_state.tab3_round = 0

    c1, c2 = st.session_state.pair
    n_diff = len(st.session_state.key_diffs)
    feature_word = "feature" if n_diff == 1 else "features"

    st.markdown(
        f"### These two sounds differ in **{n_diff} {feature_word}**. Select all that apply:"
    )

    st.markdown(
        f"""
        <div style='display: flex; justify-content: center; gap: 40px; margin-top: 1em; margin-bottom: 1em;'>
            <div style='padding: 0.5em 1em; background-color: #CCE5FF; border-radius: 8px; font-size: 2em; border: 2px solid #ccc;'>
                / {c1['symbol']} /
            </div>
            <div style='padding: 0.5em 1em; background-color: #CCCCFF; border-radius: 8px; font-size: 2em; border: 2px solid #ccc;'>
                / {c2['symbol']} /
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("**Select all differing features:**")

    tab3_choice = []
    for option in diff_options:
        checked = st.checkbox(option, key=f"tab3_cb_{st.session_state.tab3_round}_{option}")
        if checked:
            tab3_choice.append(option)

    # Buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Check answer", key="tab3_check_btn"):
            st.session_state.tab3_total += 1
            if set(tab3_choice) == set(st.session_state.key_diffs):
                st.session_state.tab3_score += 1
                st.success(f"✅ Correct! The key difference(s): {', '.join(st.session_state.key_diffs)}")
            else:
                st.error(
                    f"❌ Incorrect. These sounds differ in {n_diff} {feature_word}. Try again."
                )

            # 🎉 Trigger balloons if user reaches 20/20
            if st.session_state.tab3_score == 20 and st.session_state.tab3_total == 20:
                st.balloons()

    with col2:
        if st.button("Next", key="tab3_next_btn"):
            new_pair()
            st.rerun()

    with col3:
        if st.button("🔁 Reset Session", key="tab3_reset_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
