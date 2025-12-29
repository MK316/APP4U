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
# Config
# ---------------------------
DATASETS = {
    "Syntax": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_syntax.csv",
    "Pragmatics": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_pragmatics.csv",
    "Grammar": "https://raw.githubusercontent.com/MK316/APP4U/main/pages/data/TExam_grammar.csv",
}

IMAGE_BASE_URLS = {
    "Syntax": "https://raw.githubusercontent.com/MK316/APP4U/main/data/syntax/",
    "Pragmatics": "https://raw.githubusercontent.com/MK316/APP4U/main/data/pragmatics/",
    "Grammar": "https://raw.githubusercontent.com/MK316/APP4U/main/data/grammar/",
}

# ---------------------------
# Network helpers
# ---------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        status = getattr(resp, "status", 200)
        if status != 200:
            raise RuntimeError(f"HTTP status {status} for URL:\n{url}")
        return resp.read()

@st.cache_data(show_spinner=False, ttl=3600)
def load_csv(url: str) -> pd.DataFrame:
    raw = fetch_bytes(url)
    df = pd.read_csv(BytesIO(raw), encoding="utf-8-sig")
    for col in ["YEAR", "KEYWORDS", "TEXT", "Filename"]:
        if col in df.columns:
            df[col] = df[col].astype(str).fillna("")
    return df

# ---------------------------
# Filename cleaning + URL candidates
# ---------------------------
def strip_path(filename: str) -> str:
    """
    If CSV accidentally includes a path like 'data/syntax/2014_1.png',
    keep only the final file name.
    """
    fn = (filename or "").strip().replace("\\", "/")
    return fn.split("/")[-1]

def encode_filename(fn: str) -> str:
    return quote(fn)

def filename_variants(filename: str) -> list[str]:
    """
    Generate safe filename variants to avoid 404:
    - strip path
    - space -> underscore
    - try extension case variants
    """
    fn0 = strip_path(filename)
    if not fn0:
        return []

    variants = []

    # original + space->underscore
    variants.append(fn0)
    if " " in fn0:
        variants.append(fn0.replace(" ", "_"))

    # extension normalizations (case-sensitive on GitHub)
    def add_ext_variants(fn: str):
        lower = fn.lower()
        if lower.endswith(".png"):
            stem = fn[:-4]
            variants.extend([stem + ".png", stem + ".PNG"])
        elif lower.endswith(".jpg"):
            stem = fn[:-4]
            variants.extend([stem + ".jpg", stem + ".JPG"])
        elif lower.endswith(".jpeg"):
            stem = fn[:-5]
            variants.extend([stem + ".jpeg", stem + ".JPEG"])
        else:
            # if no extension, assume png
            variants.extend([fn + ".png", fn + ".PNG"])

    # apply ext variants to existing
    base_list = variants[:]
    for v in base_list:
        add_ext_variants(v)

    # de-dup preserving order
    seen, out = set(), []
    for v in variants:
        v = v.strip()
        if v and v not in seen:
            seen.add(v)
            out.append(v)

    return out

def candidate_urls(base_url: str, filename: str) -> list[str]:
    return [f"{base_url}{encode_filename(fn)}" for fn in filename_variants(filename)]

# ---------------------------
# Search
# ---------------------------
def search_years(df: pd.DataFrame, search_mode: str, query: str) -> list[str]:
    query = (query or "").strip().lower()
    if not query:
        st.error("Type a search query first.")
        return []

    needed = {"YEAR": "YEAR", "Keywords": "KEYWORDS", "Words containing": "TEXT"}
    col = needed.get(search_mode)
    if col and col not in df.columns:
        st.error(f"Your dataset is missing the required column: {col}")
        return []

    if search_mode == "YEAR":
        matches = df[df["YEAR"].str.startswith(query[:4])]
    elif search_mode == "Keywords":
        keys = [k.strip() for k in query.split(",") if k.strip()]
        if not keys:
            st.error("Enter at least one keyword (comma-separated).")
            return []
        matches = df[df["KEYWORDS"].str.lower().apply(lambda x: any(k in x for k in keys))]
    else:  # Words containing
        matches = df[df["TEXT"].str.lower().str.contains(query, na=False)]

    if matches.empty:
        st.error("No results found.")
        return []

    years = matches["YEAR"].tolist()
    seen, deduped = set(), []
    for y in years:
        if y not in seen:
            seen.add(y)
            deduped.append(y)
    return deduped

# ---------------------------
# Image display (crisp)
# ---------------------------
def show_image_from_url(url: str, caption: str, key_prefix: str):
    img_bytes = fetch_bytes(url)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")

    st.caption(f"Original pixels: {img.size[0]} × {img.size[1]}")

    zoom = st.slider("Zoom", 50, 250, 140, 10, key=f"{key_prefix}_zoom")
    w, h = img.size
    new_w = max(1, int(w * zoom / 100))
    new_h = max(1, int(h * zoom / 100))

    # NEAREST keeps scanned text crisp
    img_zoomed = img.resize((new_w, new_h), resample=Image.NEAREST)
    st.image(img_zoomed, caption=caption)

# ---------------------------
# Tab renderer
# ---------------------------
def render_search_tab(tab_name: str, data_url: str):
    try:
        df = load_csv(data_url)
    except Exception as e:
        st.error(f"Failed to load dataset:\n{data_url}\n\n{e}")
        return

    key_prefix = tab_name.lower()

    st.subheader(f"{tab_name}")

    with st.form(key=f"{key_prefix}_form"):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write("Search mode:")
        with col2:
            search_mode = st.radio(
                "",
                ["YEAR", "Keywords", "Words containing"],
                horizontal=True,
                key=f"{key_prefix}_mode",
            )
        query = st.text_input("Search query", "", key=f"{key_prefix}_q")
        submitted = st.form_submit_button("🍒 Search")

    if submitted:
        results = search_years(df, search_mode, query)
        st.session_state[f"{key_prefix}_results"] = results
        if results:
            st.session_state[f"{key_prefix}_year"] = results[0]

    results = st.session_state.get(f"{key_prefix}_results", [])
    if not results:
        st.info("Run a search to see results.")
        return

    selected_year = st.selectbox(
        "Select a year from results",
        results,
        key=f"{key_prefix}_year",
    )

    if st.button("🍒 Show me the exam question", key=f"{key_prefix}_show"):
        match = df[df["YEAR"] == selected_year]
        if match.empty:
            st.error("No record found for this year.")
            return

        row = match.iloc[0]
        keywords = row.get("KEYWORDS", "")
        filename = row.get("Filename", "")

        st.markdown(f"🌷 Keywords: 🔑 {keywords}")

        if not filename or filename.lower() in {"nan", "none"}:
            st.error("Filename is missing in the dataset for this item.")
            return

        base = IMAGE_BASE_URLS[tab_name]
        urls = candidate_urls(base, filename)

        with st.expander("Image URL (debug)"):
            st.write("Filename in CSV:", filename)
            st.write("Tried:")
            for u in urls:
                st.write(u)

        chosen = None
        last_err = None
        for u in urls:
            try:
                _ = fetch_bytes(u)
                chosen = u
                break
            except Exception as e:
                last_err = e

        if not chosen:
            st.error(
                "Failed to load image.\n"
                f"Base folder: {base}\n"
                f"Filename in CSV: {filename}\n"
                f"Last error: {last_err}"
            )
            return

        show_image_from_url(
            chosen,
            caption=f"{tab_name} Exam Image for {selected_year}",
            key_prefix=key_prefix,
        )

# ---------------------------
# UI: tabs
# ---------------------------
tab_syntax, tab_prag, tab_gram = st.tabs(["Syntax", "Pragmatics", "Grammar"])

with tab_syntax:
    render_search_tab("Syntax", DATASETS["Syntax"])

with tab_prag:
    render_search_tab("Pragmatics", DATASETS["Pragmatics"])

with tab_gram:
    render_search_tab("Grammar", DATASETS["Grammar"])
