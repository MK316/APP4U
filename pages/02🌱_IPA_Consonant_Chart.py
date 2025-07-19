
import streamlit as st

st.set_page_config(page_title="Final IPA Vowel Chart")

st.title("🌱 IPA English Consonant Chart")

tab1, tab2, tab3 = st.tabs(["English Consonants", "Allophones", "Diacritics"])

with tab1:
    st.markdown("Consonant chart")

with tab1:
    st.image("https://raw.githubusercontent.com/MK316/English-linguistics/main/pages/images/Cchart.png", caption="Consonant Chart", use_container_width=True)


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

with tab3:
    st.markdown("📌 You can add more vowel visualizations or explanation notes here.")
