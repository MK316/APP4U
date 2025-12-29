import streamlit as st
import pandas as pd
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from io import BytesIO
from PIL import Image

# ---------------------------
# Page setup (MUST be first Streamlit call)
# ---------------------------
st.set_page_config(page_title="TCE Search", layout="wide")

st.title("TCE Search")

# ---------------------------
# Config: datasets per tab
# ---------------------------
DATASETS = {
    "Syntax": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_syntax.csv",
    "Pragmatics": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_pragmatics.csv",
    "Grammar": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_grammar.csv",
}

# IMPORTANT: use raw.githubusercontent.com for direct file access
IMAGE_BASE_URLS = {
    "Syntax": "https://raw.githubusercontent.com/MK316/APP4U/main/data/syntax/",
    "Pragmatics": "https://raw.githubusercontent.com/MK316/APP4U/main/data/pragmatics/",
    "Grammar": "https://raw.githubusercontent.com/MK316/APP4U/main/data/grammar/",
}

# ---------------------------
# Utilities
# ---------------------------
def normalize_filename(filename: str) -> str:
    """
    Make filenames from CSV resilient:
    - trim
    - space -> underscore
    - keep original case in stem, but normalize extension to lowercase
    - URL-encode
    """
    fn = (filename or "").strip()
    fn = fn.replace(" ", "_")

    # normalize only extension casing (png/jpg/jpeg)
    lower = fn.lower()
    if lower.endswith(".png"):
        fn = fn[:-4] + ".png"
    elif lower.endswith(".jpg"):
        fn = fn[:-4] + ".jpg"
    elif lower.endswith(".jpeg"):
        fn = fn[:-5] + ".jpeg"

    return quote(fn)

def candidate_image_urls(base: str, filename: str) -> list[str]:
    """
    Try a small set of plausible URLs to avoid 404 from minor CSV inconsistencies.
    """
    fn0 = (filename or "").strip()
    if not fn0:
        return []

    # 1) original
    cands = [fn0]

    # 2) space -> underscore
    if " " in fn0:
        cands.append(fn0.replace(" ", "_"))

    # 3) extension normalized
    lower = fn0.lower()
    if lower.endswith(".png") and not fn0.endswith(".png"):
        cands.append(fn0[:-4] + ".png")
    if lower.endswith(".jpg") and not fn0.endswith(".jpg"):
        cands.append(fn0[:-4] + ".jpg")
    if lower.endswith(".jpeg") and not fn0.endswith(".jpeg"):
        cands.append(fn0[:-5] + ".jpeg")

    # de-dup while preserving order
    seen, uniq = set(), []
    for x in cands:
        if x not in seen:
            seen.add(x)
            uniq.append(x)

    return [f"{base}{normalize_filename(x)}" for x in uniq]

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_bytes(url: str) -> bytes:
    """
    Fetch bytes with a browser-like User-Agent.
    """
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

        # make expected columns robust
        for col in ["YEAR", "KEYWORDS", "TEXT", "Filename"]:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna("")

        return df
    except HTTPError as e:
        raise RuntimeError(f"HTTPError {e.code} when loading CSV:\n{url}") from e
    except URLError as e:
        raise RuntimeError(f"URLError when loading CSV:\n{url}\nReason: {e.reason}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV:\n{url}\nError: {e}") from e

def search_years(df: pd.DataFrame, search_mode: str, query: str) -> list[str]:
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
        q = query[:4]
        matches = df[df["YEAR"].str.startswith(q)]
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
    # keep order, remove duplicates
    seen, deduped = set(), []
    for y in years:
        if y not in seen:
            seen.add(y)
            deduped.append(y)
    return deduped

def show_zoomable_image(image_url: str, caption: str, key_prefix: str):
    """
    Display a crisp zoomable image:
    - Avoid use_container_width for text scans (it often triggers blur via resampling)
    - Resize with NEAREST for crisp text edges
    """
    img_bytes = fetch_bytes(image_url)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")

    st.caption(f"Original pixels: {img.size[0]} × {img.size[1]}")

    zoom = st.slider("Zoom", 50, 250, 140, 10, key=f"{key_prefix}_zoom")
    w, h = img.size
    new_w = max(1, int(w * zoom / 100))
    new_h = max(1, int(h * zoom / 100))

    # NEAREST keeps text sharper for scanned/exam images
    img_zoomed = img.resize((new_w, new_h), resample=Image.NEAREST)

    # Do NOT force container width; show at the resized pixel size
    st.image(img_zoomed, caption=caption)

def render_search_tab(tab_name: str, data_url: str):
    try:
        df = load_csv(data_url)
    except RuntimeError as e:
        st.error(str(e))
        st.stop()

    key_prefix = tab_name.lower()

    st.subheader(f"{tab_name}")

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

    st.markdown("---")
    st.subheader("Choose an item from the results")

    results_key = f"{key_prefix}_results"
    selected_key = f"{key_prefix}_selected_year"

    if results_key not in st.session_state or not st.session_state[results_key]:
        st.info("Run a search first to see results here.")
        return

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
        image_filename = (row.get("Filename", "") or "").strip()
        keywords = row.get("KEYWORDS", "")

        if not image_filename or image_filename.lower() in {"nan", "none"}:
            st.error("No image filename found for this item.")
            return

        base = IMAGE_BASE_URLS.get(tab_name, IMAGE_BASE_URLS["Syntax"])
        url_candidates = candidate_image_urls(base, image_filename)

        st.markdown(f"🌷 Keywords: 🔑 {keywords}")

        with st.expander("Image URL (debug)", expanded=False):
            st.write("Filename in CSV:", image_filename)
            st.write("Tried URLs:")
            for u in url_candidates:
                st.write(u)

        # Try candidate URLs until one works
        last_err = None
        chosen_url = None
        for u in url_candidates:
            try:
                # lightweight check by fetching first bytes
                _ = fetch_bytes(u)
                chosen_url = u
                break
            except Exception as e:
                last_err = e

        if not chosen_url:
            st.error(f"Failed to locate image for: {image_filename}\nLast error: {last_err}")
            return

        # Show crisp zoomable image
        try:
            show_zoomable_image(
                chosen_url,
                caption=f"{tab_name} Exam Image for {selected_year}",
                key_prefix=key_prefix,
            )
        except Exception as e:
            st.error(f"Failed to load image.\n{chosen_url}\nError: {e}")

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
