st.set_page_config(layout="wide")

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from os import BytesIO
import requests



st.set_page_config(page_title="Final IPA Vowel Chart")

st.title("🌱 Final IPA Vowel Chart")

tab1, tab2, tab3 = st.tabs(["Monophthongs", "Tense/Lax", "Diphthongs"])

with tab1:
    st.markdown("""
    <style>
    table {
        border-collapse: collapse;
        margin-top: 1rem;
        width: 600px;
    }
    td {
        border: none;
        padding: 0.8em;
        text-align: center;
        vertical-align: middle;
        font-size: 1.3em;
    }
    th {
        border: none;
        padding: 0.8em;
        font-size: 1.3em;
        font-weight: bold;
    }
    .orange {
        color: orange;
        font-weight: bold;
    }
    .rowlabel {
        text-align: center;
        vertical-align: middle;
        font-weight: bold;
    }
    .bottomcell {
        vertical-align: bottom;
        height: 4em;
    }
    </style>

    <table>
        <thead>
            <tr>
                <th style="text-align:center; vertical-align:middle;"></th>
                <th style="text-align:center; vertical-align:middle;">Front</th>
                <th style="text-align:center; vertical-align:middle;">(Central)</th>
                <th style="text-align:center; vertical-align:middle;">Back</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="rowlabel">High</td>
                <td>i<br>ɪ</td>
                <td></td>
                <td>u<br>ʊ</td>
            </tr>
            <tr>
                <td class="rowlabel">(Mid)</td>
                <td><span class="orange">e</span><br>ɛ</td>
                <td>ə<br>ʌ (ɜ)</td>
                <td><span class="orange">o</span><br>ɔ</td>
            </tr>
            <tr>
                <td class="rowlabel">Low</td>
                <td>æ</td>
                <td class="bottomcell"><span class="orange">a</span></td>
                <td class="bottomcell">ɑ / ɒ</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    #### 🚩 Notes: 

    Vowel inventories vary significantly depending on English dialects.

    1. /e/ and /o/ are considered either monophthongs or parts of diphthongs depending on the dialect — e.g., /eɪ/, /oʊ/.

    2. /ɒ/ is a rounded version of /ɑ/.

    3. /ɜ/ is a contextual variant — for example, it appears in r-colored vowels or after r-deletion in some dialects.
    """)

with tab2:
    st.markdown("""
    <style>
    table {
        border-collapse: collapse;
        margin-top: 1rem;
        width: 600px;
    }
    td {
        border: none;
        padding: 0.8em;
        text-align: center;
        vertical-align: middle;
        font-size: 1.3em;
    }
    th {
        border: none;
        padding: 0.8em;
        font-size: 1.3em;
        font-weight: bold;
    }
    .orange {
        color: red;
        font-weight: bold;
    }
    .rowlabel {
        text-align: center;
        vertical-align: middle;
        font-weight: bold;
    }
    .bottomcell {
        vertical-align: bottom;
        height: 4em;
    }
    </style>

    <table>
        <thead>
            <tr>
                <th style="text-align:center; vertical-align:middle;"></th>
                <th style="text-align:center; vertical-align:middle;">Front</th>
                <th style="text-align:center; vertical-align:middle;">(Central)</th>
                <th style="text-align:center; vertical-align:middle;">Back</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="rowlabel">High</td>
                <td><span class="orange">i</span><br>ɪ</td>
                <td></td>
                <td><span class="orange">u</span><br>ʊ</td>
            </tr>
            <tr>
                <td class="rowlabel">(Mid)</td>
                <td>e<br>ɛ</td>
                <td>ə<br>ʌ (ɜ)</td>
                <td>o<br><span class="orange">(ɔ)</span></td>
            </tr>
            <tr>
                <td class="rowlabel">Low</td>
                <td>æ</td>
                <td class="bottomcell">a</td>
                <td class="bottomcell"><span class="orange">ɑ / ɒ</span></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# Move this to the very top of your file
st.set_page_config(layout="wide")

# Inside tab3
with tab3:
    st.header("🎯 Draw English Diphthongs on the Vowel Chart")

    # --- Step 1: Load image from GitHub ---
    image_url = "https://raw.githubusercontent.com/MK316/APP4U/main/pages/images/vowelchart.png"

    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
    except Exception as e:
        st.error("❌ Failed to load the vowel chart image.")
        st.stop()

    # --- Step 2: Display canvas ---
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
        stroke_color="#0000FF",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="freedraw",  # You can change to "line" if preferred
        key="vowel_canvas",
    )

    # --- Step 3: Clear canvas button ---
    st.markdown("---")
    if st.button("🧹 Clear Canvas"):
        st.experimental_rerun()
