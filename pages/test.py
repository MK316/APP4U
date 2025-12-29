import streamlit as st
import pandas as pd

st.set_page_config(page_title="TCE Search", layout="wide")

# ---------------------------
# Config: datasets per tab
# ---------------------------
DATASETS = {
    "Syntax": "https://raw.githubusercontent.com/MK316/APP4U/refs/heads/main/pages/data/TExam_syntax.csv",
    "Pragmatics": "https://raw.githubusercontent.com/MK316/APP4U/refs/heads/main/pages/data/TExam_pragmatics.csv",
    "Grammar": "https://raw.githubusercontent.com/MK316/APP4U/refs/heads/main/pages/data/TExam_grammar.csv",
}

IMAGE_BASE_URL = "https://raw.githubusercontent.com/MK316/APP4U/main/data/syntax/"

@st.cache_data(show_spinner=False)
def load_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url, encoding="utf-8-sig")
    # defensive cleaning
    for col in ["YEAR", "KEYWORDS", "TEXT", "Filename"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

def search_years(df: pd.DataFrame, search_mode: str, query: str):
    query = (query or "").strip().lower()
    if not query:
        st.error("Type a search query first.")
        return []

    # Guard against missing columns
    required = {
        "YEAR": ["YEAR"],
        "Keywords": ["KEYWORDS"],
        "Words containing": ["TEXT"],
    }
    if search_mode in required:
        for c in required[search_mode]:
            if c not in df.columns:
                st.error(f"Your dataset is missing the required column: {c}")
                return []

    if search_mode == "YEAR":
        q = query[:4]
        matches = df[df["YEAR"].str.startswith(q)]
    elif search_mode == "Keywords":
        # comma-separated keywords
        keyword_list = [k.strip() for k in query.split(",") if k.strip()]
        if not keyword_list:
            st.error("Enter at least one keyword (comma-separated if multiple).")
            return []
        matches = df[df["KEYWORDS"].str.lower().apply(lambda x: any(k in x for k in keyword_list))]
    elif search_mode == "Words containing":
        matches = df[df["TEXT"].str.lower().str.contains(query, na=False)]
    else:
        st.error("Please select a valid search mode.")
        return []

    if matches.empty:
        st.error("No results found for your query.")
        return []

    # keep order, remove duplicates
    years = matches["YEAR"].tolist()
    seen = set()
    deduped = []
    for y in years:
        if y not in seen:
            seen.add(y)
            deduped.append(y)
    return deduped

def render_search_tab(tab_name: str, data_url: str):
    df = load_data(data_url)

    # Unique keys per tab (so session_state does not collide)
    key_prefix = tab_name.lower()

    st.subheader(f"❄️ [{tab_name}] Start Searching")

    with st.form(key=f"{key_prefix}_search_form"):
        col1, col2 = st.columns([1, 3])

        with col1:
            st.write("Search mode by:")

        with col2:
            search_mode = st.radio(
                "",
                ["YEAR", "Keywords", "Words containing"],
                horizontal=True,
                key=f"{key_prefix}_search_mode",
            )

        query = st.text_input(
            "Search Query: e.g., 2024 (YEAR), tapping (Keywords), distribution (Words containing)",
            "",
            key=f"{key_prefix}_query",
        )
        search_button = st.form_submit_button("🍒 Click to Search")

    if search_button:
        results = search_years(df, search_mode, query)
        if results:
            st.session_state[f"{key_prefix}_results"] = results
            st.session_state[f"{key_prefix}_selected_year"] = results[0]
            st.success("Search completed successfully.")

    st.subheader("❄️ [2] Choose an item from the selected:")

    results_key = f"{key_prefix}_results"
    selected_key = f"{key_prefix}_selected_year"

    if results_key in st.session_state and st.session_state[results_key]:
        selected_year = st.selectbox(
            "Select a year from the results",
            st.session_state[results_key],
            index=0,
            key=selected_key,
        )

        if st.button("🍒 Show me the exam question", key=f"{key_prefix}_show_button"):
            match = df[df["YEAR"] == selected_year]
            if not match.empty:
                row = match.iloc[0]
                image_filename = row.get("Filename", "")
                keywords = row.get("KEYWORDS", "")

                if image_filename:
                    image_url = f"{IMAGE_BASE_URL}{image_filename}"
                    st.markdown(f"**🌷 Keywords:** 🔑 {keywords}")
                    st.image(image_url, caption=f"{tab_name} Exam Image for {selected_year}", width=800)
                else:
                    st.error("No image filename found for this item.")
            else:
                st.error("No matching record found for this year.")
    else:
        st.info("Run a search first to see results here.")

# ---------------------------
# UI: 3 tabs
# ---------------------------
tab_syntax, tab_prag, tab_gram = st.tabs(["Syntax", "Pragmatics", "Grammar"])

with tab_syntax:
    render_search_tab("Syntax", DATASETS["Syntax"])

with tab_prag:
    render_search_tab("Pragmatics", DATASETS["Pragmatics"])

with tab_gram:
    render_search_tab("Grammar", DATASETS["Grammar"])
