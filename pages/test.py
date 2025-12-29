import streamlit as st
import pandas as pd
import urllib.request
from urllib.parse import quote
from io import BytesIO
from PIL import Image

# ---------------------------
# Page setup (MUST be first Streamlit call)
# ---------------------------
st.set_page_config(page_title="Teacher Certification Exam Search", layout="wide")
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
        return resp.read()

@st.cache_data(show_spinner=False, ttl=3600)
def load_csv(url: str) -> pd.DataFrame:
    raw = fetch_bytes(url)
    df = pd.read_csv(BytesIO(raw), encoding="utf-8-sig")
    for col in ["YEAR", "KEYWORDS", "TEXT", "Filename"]:
        if col in df.columns:
            df[col] = df[col].astype(str).fillna("")
    return df

@st.cache_data(show_spinner=False, ttl=3600)
def load_pil_image(url: str) -> Image.Image:
    b = fetch_bytes(url)
    return Image.open(BytesIO(b)).convert("RGB")

# ---------------------------
# Filename helpers
# ---------------------------
def strip_path(filename: str) -> str:
    fn = (filename or "").strip().replace("\\", "/")
    return fn.split("/")[-1]

def filename_variants(filename: str) -> list[str]:
    fn0 = strip_path(filename)
    if not fn0:
        return []

    variants = [fn0]
    if " " in fn0:
        variants.append(fn0.replace(" ", "_"))

    out = []
    for v in variants:
        lower = v.lower()
        if lower.endswith(".png"):
            stem = v[:-4]
            out.extend([stem + ".png", stem + ".PNG"])
        elif lower.endswith(".jpg"):
            stem = v[:-4]
            out.extend([stem + ".jpg", stem + ".JPG"])
        elif lower.endswith(".jpeg"):
            stem = v[:-5]
            out.extend([stem + ".jpeg", stem + ".JPEG"])
        else:
            out.extend([v + ".png", v + ".PNG"])

    out.extend(variants)

    seen, uniq = set(), []
    for x in out:
        x = x.strip()
        if x and x not in seen:
            seen.add(x)
            uniq.append(x)

    return uniq

def candidate_urls(base_url: str, filename: str) -> list[str]:
    return [f"{base_url}{quote(fn)}" for fn in filename_variants(filename)]

# ---------------------------
# Search helpers
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
    else:
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
# Image rendering (NO SLIDER)
# ---------------------------
def render_image_view(tab_key: str):
    img_url = st.session_state.get(f"{tab_key}_img_url", "")
    year = st.session_state.get(f"{tab_key}_img_year", "")
    tab_name = st.session_state.get(f"{tab_key}_img_tabname", tab_key)
    keywords = st.session_state.get(f"{tab_key}_img_keywords", "")

    if not img_url:
        return

    if keywords:
        st.markdown(f"🌷 Keywords: 🔑 {keywords}")

    with st.expander("Image URL (debug)", expanded=False):
        st.write(img_url)

    try:
        img = load_pil_image(img_url)
        st.caption(f"Original pixels: {img.size[0]} × {img.size[1]}")
        # Native display (best for sharp text)
        st.image(img, caption=f"{tab_name} Exam Image for {year}")
    except Exception as e:
        st.error(f"Failed to load image.\n{img_url}\nError: {e}")

# ---------------------------
# Tab renderer
# ---------------------------
def render_search_tab(tab_name: str, data_url: str):
    tab_key = tab_name.lower()

    try:
        df = load_csv(data_url)
    except Exception as e:
        st.error(f"Failed to load dataset:\n{data_url}\n\n{e}")
        return

    st.subheader(tab_name)

    with st.form(key=f"{tab_key}_form"):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write("Search mode:")
        with col2:
            search_mode = st.radio(
                "",
                ["YEAR", "Keywords", "Words containing"],
                horizontal=True,
                key=f"{tab_key}_mode",
            )
        query = st.text_input("Search query", "", key=f"{tab_key}_query")
        submitted = st.form_submit_button("🍒 Search")

    if submitted:
        results = search_years(df, search_mode, query)
        st.session_state[f"{tab_key}_results"] = results
        if results:
            st.session_state[f"{tab_key}_year"] = results[0]

    results = st.session_state.get(f"{tab_key}_results", [])
    if not results:
        st.info("Run a search to see results.")
        return

    selected_year = st.selectbox(
        "Select a year from results",
        results,
        key=f"{tab_key}_year",
    )

    if st.button("🍒 Show me the exam question", key=f"{tab_key}_show"):
        match = df[df["YEAR"] == selected_year]
        if match.empty:
            st.error("No record found for this year.")
            return

        row = match.iloc[0]
        keywords = row.get("KEYWORDS", "")
        filename = row.get("Filename", "")

        if not filename or filename.lower() in {"nan", "none"}:
            st.error("Filename is missing in the dataset for this item.")
            return

        base = IMAGE_BASE_URLS[tab_name]
        urls = candidate_urls(base, filename)

        chosen = None
        last_err = None
        for u in urls:
            try:
                _ = load_pil_image(u)
                chosen = u
                break
            except Exception as e:
                last_err = e

        if not chosen:
            st.error(
                "Failed to locate image.\n"
                f"Base folder: {base}\n"
                f"Filename in CSV: {filename}\n"
                f"Last error: {last_err}"
            )
            return

        # Persist selection so reruns keep showing the image
        st.session_state[f"{tab_key}_img_url"] = chosen
        st.session_state[f"{tab_key}_img_year"] = selected_year
        st.session_state[f"{tab_key}_img_tabname"] = tab_name
        st.session_state[f"{tab_key}_img_keywords"] = keywords

    # Always show the last loaded image (if any)
    render_image_view(tab_key)

# ---------------------------
# UI
# ---------------------------
tab_syntax, tab_prag, tab_gram = st.tabs(["🔳 Syntax", "🔳 Pragmatics", "🔳 Grammar"])

with tab_syntax:
    render_search_tab("🔳 Syntax", DATASETS["Syntax"])

with tab_prag:
    render_search_tab("🔳 Pragmatics", DATASETS["Pragmatics"])

with tab_gram:
    render_search_tab("🔳 Grammar", DATASETS["Grammar"])
