import streamlit as st
import pandas as pd
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from io import BytesIO

st.set_page_config(page_title="TCE Search", layout="wide")

# ---------------------------
# Config: datasets per tab
# ---------------------------
DATASETS = {
    "Syntax": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_syntax.csv",
    "Pragmatics": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_pragmatics.csv",
    "Grammar": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_grammar.csv",
}

# IMPORTANT: GitHub "tree" URLs do NOT work as image sources.
# Use raw.githubusercontent.com instead.
IMAGE_BASE_URLS = {
    "Syntax": "https://raw.githubusercontent.com/MK316/APP4U/main/data/syntax/",
    "Pragmatics": "https://raw.githubusercontent.com/MK316/APP4U/main/data/pragmatics/",
    "Grammar": "https://raw.githubusercontent.com/MK316/APP4U/main/data/grammar/",
}

def normalize_filename(filename: str) -> str:
    fn = (filename or "").strip()
    fn = fn.replace(" ", "_")       # space → underscore
    fn = fn.lower()                 # normalize case
    return quote(fn)                # URL-safe
    
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_bytes(url: str) -> bytes:
    """Fetch bytes from a URL with a browser-like User-Agent."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        status = getattr(resp, "status", 200)
        if status != 200:
            raise RuntimeError(f"HTTP status {status} for URL:\n{url}")
        return resp.read()

@st.cache_data(show_spinner=False, ttl=3600)
def load_csv(url: str) -> pd.DataFrame:
    try:
        raw = fetch_bytes(url)
        df = pd.read_csv(BytesIO(raw), encoding="utf-8-sig")
        for col in ["YEAR", "KEYWORDS", "TEXT", "Filename"]:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    except HTTPError as e:
        raise RuntimeError(f"HTTPError {e.code} when loading CSV:\n{url}") from e
    except URLError as e:
        raise RuntimeError(f"URLError when loading CSV:\n{url}\nReason: {e.reason}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV:\n{url}\nError: {e}") from e

def search_years(df: pd.DataFrame, search_mode: str, query: str):
    query = (query or "").strip().lower()
    if not query:
        st.error("Type a search query first.")
        return []

    required = {"YEAR": "YEAR", "Keywords": "KEYWORDS", "Words containing": "TEXT"}
    needed_col = required.get(search_mode)
    if needed_col and needed_col not in df.columns:
        st.error(f"Your dataset is missing the required column: {needed_col}")
        return []

    if search_mode == "YEAR":
        matches = df[df["YEAR"].str.startswith(query[:4])]
    elif search_mode == "Keywords":
        keys = [k.strip() for k in query.split(",") if k.strip()]
        if not keys:
            st.error("Enter at least one keyword (comma-separated if multiple).")
            return []
        matches = df[df["KEYWORDS"].str.lower().apply(lambda x: any(k in x for k in keys))]
    elif search_mode == "Words containing":
        matches = df[df["TEXT"].str.lower().str.contains(query, na=False)]
    else:
        st.error("Please select a valid search mode.")
        return []

    if matches.empty:
        st.error("No results found for your query.")
        return []

    years = matches["YEAR"].tolist()
    deduped, seen = [], set()
    for y in years:
        if y not in seen:
            seen.add(y)
            deduped.append(y)
    return deduped

def render_search_tab(tab_name: str, data_url: str):
    try:
        df = load_csv(data_url)
    except RuntimeError as e:
        st.error(str(e))
        st.stop()

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
            if match.empty:
                st.error("No matching record found for this year.")
                return

            row = match.iloc[0]
            image_filename = row.get("Filename", "").strip()
            keywords = row.get("KEYWORDS", "")

            if not image_filename or image_filename.lower() in {"nan", "none"}:
                st.error("No image filename found for this item.")
                return

            base = IMAGE_BASE_URLS.get(tab_name, IMAGE_BASE_URLS["Syntax"])
            safe_name = normalize_filename(image_filename)
            image_url = f"{base}{safe_name}"


            st.markdown(f"**🌷 Keywords:** 🔑 {keywords}")

            # Show the exact URL (helps you confirm it is raw + correct)
            with st.expander("Image URL (debug)", expanded=False):
                st.write(image_url)

            # Load the image (this also catches 404/403 and shows a readable error)
            try:
                img_bytes = fetch_bytes(image_url)
                st.image(img_bytes, caption=f"{tab_name} Exam Image for {selected_year}", width=800)
            except Exception as e:
                st.error(f"Failed to load image.\n{image_url}\nError: {e}")

    else:
        st.info("Run a search first to see results here.")

tab_syntax, tab_prag, tab_gram = st.tabs(["Syntax", "Pragmatics", "Grammar"])

with tab_syntax:
    render_search_tab("Syntax", DATASETS["Syntax"])

with tab_prag:
    render_search_tab("Pragmatics", DATASETS["Pragmatics"])

with tab_gram:
    render_search_tab("Grammar", DATASETS["Grammar"])
