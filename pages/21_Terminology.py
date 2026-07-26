import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components

DATA_URL = "https://raw.githubusercontent.com/MK316/APP4U/refs/heads/main/data/phon_terminology.csv"

st.set_page_config(page_title="Phonetics & Phonology Flashcards", page_icon="🃏", layout="centered")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df = df.dropna(subset=["Terminology", "Description"])
    return df.reset_index(drop=True)

df = load_data()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
defaults = {
    "stage": "setup",     # setup -> quiz -> done
    "deck": [],
    "idx": 0,
    "score": 0,
    "attempts": 0,
    "graded_this_card": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def start_practice(n):
    sample = df.sample(n=n, replace=False).to_dict("records")
    st.session_state.deck = sample
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.graded_this_card = False
    st.session_state.stage = "quiz"


def restart():
    st.session_state.stage = "setup"
    st.session_state.deck = []
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.graded_this_card = False


def grade(correct):
    if not st.session_state.graded_this_card:
        st.session_state.attempts += 1
        if correct:
            st.session_state.score += 1
        st.session_state.graded_this_card = True


def next_card():
    st.session_state.idx += 1
    st.session_state.graded_this_card = False


# ---------------------------------------------------------------------------
# Flip-card component (pure client-side flip; scoring buttons are native
# Streamlit widgets rendered underneath so reruns are always reliable)
# ---------------------------------------------------------------------------
def render_flip_card(description, example, term, card_key):
    html = f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
      * {{ box-sizing: border-box; }}
      body {{ margin: 0; font-family: 'Inter', sans-serif; }}
      .stage {{ perspective: 1600px; width: 100%; height: 380px; }}
      .flip-card {{
        position: relative; width: 100%; height: 100%;
        cursor: pointer; transition: transform 0.65s cubic-bezier(.4,.2,.2,1);
        transform-style: preserve-3d;
      }}
      .flip-card.flipped {{ transform: rotateY(180deg); }}
      .face {{
        position: absolute; inset: 0; border-radius: 20px;
        backface-visibility: hidden; padding: 30px 34px;
        display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 10px 30px rgba(20,22,48,0.25);
      }}
      .front {{
        background: linear-gradient(155deg, #1B1F3B 0%, #262B52 100%);
        color: #F4EFE6;
      }}
      .back {{
        background: #F4EFE6;
        color: #1B1F3B;
        transform: rotateY(180deg);
        text-align: center;
        align-items: center;
      }}
      .eyebrow {{
        font-size: 12px; letter-spacing: 2.5px; text-transform: uppercase;
        color: #E8A33D; font-weight: 600; margin-bottom: 14px;
      }}
      .desc {{
        font-size: 16.5px; line-height: 1.55; margin-bottom: 16px;
        max-height: 190px; overflow-y: auto; padding-right: 6px;
      }}
      .example {{
        font-size: 14.5px; line-height: 1.5; color: #C9CCE6;
        border-top: 1px solid rgba(244,239,230,0.25); padding-top: 12px;
        font-style: italic;
      }}
      .term {{
        font-family: 'Playfair Display', serif; font-weight: 800;
        font-size: 34px; margin-bottom: 10px; line-height: 1.15;
      }}
      .hint {{
        font-size: 12.5px; color: #6b6f8f; letter-spacing: 1px;
        text-transform: uppercase; margin-top: 18px;
      }}
      .backline {{ width: 46px; height: 3px; background: #E8A33D; margin-bottom: 16px; border-radius: 2px; }}
    </style>
    </head>
    <body>
      <div class="stage">
        <div class="flip-card" id="card-{card_key}" onclick="this.classList.toggle('flipped')">
          <div class="face front">
            <div class="eyebrow">Term #{card_key} · Tap card to reveal</div>
            <div class="desc">{description}</div>
            <div class="example">{example}</div>
          </div>
          <div class="face back">
            <div class="backline"></div>
            <div class="term">{term}</div>
            <div class="hint">Tap again to flip back</div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    components.html(html, height=400)


# ---------------------------------------------------------------------------
# UI: setup screen
# ---------------------------------------------------------------------------
st.title("🃏 Phonetics & Phonology Flashcards")

if st.session_state.stage == "setup":
    st.write("Read the description and example, tap the card to reveal the term, then grade yourself.")
    max_n = len(df)
    n = st.slider("How many terms would you like to practice?", min_value=5, max_value=max_n, value=min(15, max_n), step=1)
    if st.button("▶️ Start practice", type="primary"):
        start_practice(n)
        st.rerun()

# ---------------------------------------------------------------------------
# UI: quiz screen
# ---------------------------------------------------------------------------
elif st.session_state.stage == "quiz":
    deck = st.session_state.deck
    total = len(deck)
    idx = st.session_state.idx

    if idx >= total:
        st.session_state.stage = "done"
        st.rerun()

    card = deck[idx]

    st.progress(idx / total, text=f"Card {idx + 1} of {total}  ·  Score: {st.session_state.score}/{st.session_state.attempts}")

    render_flip_card(
        description=card["Description"],
        example=card.get("Example", ""),
        term=card["Terminology"],
        card_key=int(card.get("Number", idx)),
    )

    st.caption("Click the card above to flip it and see the answer, then grade yourself below.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Got it right", use_container_width=True, disabled=st.session_state.graded_this_card):
            grade(True)
    with col2:
        if st.button("❌ Missed it", use_container_width=True, disabled=st.session_state.graded_this_card):
            grade(False)

    st.write("")
    next_label = "Next card ▶️" if idx < total - 1 else "Finish 🏁"
    if st.button(next_label, type="primary", use_container_width=True, disabled=not st.session_state.graded_this_card):
        next_card()
        st.rerun()

    if not st.session_state.graded_this_card:
        st.info("Grade yourself (Got it right / Missed it) before moving on.")

    st.write("")
    if st.button("🔁 Restart session"):
        restart()
        st.rerun()

# ---------------------------------------------------------------------------
# UI: results screen
# ---------------------------------------------------------------------------
elif st.session_state.stage == "done":
    score = st.session_state.score
    total = st.session_state.attempts
    st.subheader("Session complete!")
    st.markdown(f"### Your score: **{score} / {total}**")

    if total > 0 and score == total:
        st.balloons()
        st.success("🎉 Perfect score! Great work.")
    elif total > 0:
        pct = round(100 * score / total)
        st.write(f"You got {pct}% correct. Keep practicing the ones you missed!")

    if st.button("🔁 Practice again", type="primary"):
        restart()
        st.rerun()
