import streamlit as st
import pandas as pd

tab1, tab2 = st.tabs(["Overview", "TCE app"])
with tab1:
  st.caption("Teacher Certificate Exam questions: Phonetics & Phonology")

with tab2:
# Load the DataFrame
url = "https://raw.githubusercontent.com/MK316/APP4U/refs/heads/main/data/TExam_new20241125.csv"
df = pd.read_csv(url, encoding='utf-8-sig')

# Function to search years based on the selected mode
def search_years(search_mode, query):
    if search_mode == "Search questions by YEAR":
        matches = df[df['YEAR'].str.startswith(query.strip()[:4])]  # Ensure query is stripped of whitespace
    elif search_mode == "Search questions by Keywords":
        keyword_list = [keyword.strip().lower() for keyword in query.split(',')]
        matches = df[df['KEYWORDS'].str.lower().apply(lambda x: any(keyword in x for keyword in keyword_list))]
    elif search_mode == "Search questions by Words":
        word_list = [word.strip().lower() for word in query.split(',')]
        matches = df[df['TEXT'].str.lower().apply(lambda x: any(word in x for word in word_list))]
    else:
        st.write("Please select a valid search mode.")
        return []

    if matches.empty:
        st.write("No results found for your query.")
        return []
    return matches['YEAR'].tolist()

# Streamlit layout
st.title('Teacher Certificate Exam Searching Engine')
st.subheader('❄️ [1] Search Data')

search_mode = st.radio("Search Mode", ["Search questions by YEAR", "Search questions by Keywords", "Search questions by Words"])
query = st.text_input("Search Query: e.g., 2024 (by YEAR) or tapping (by Keywords or Words)", "")
if st.button('Click to Search'):
    results = search_years(search_mode, query)
    if results:
        st.write("Search completed successfully.")
        selected_year = st.selectbox("Select a year from the results", results)

        # Function to display an exam question based on the selected year
        if st.button('Show me the exam question'):
            match = df[df['YEAR'] == selected_year]
            if not match.empty:
                image_filename = match.iloc[0]['Filename']
                image_url = f'https://huggingface.co/spaces/MK-316/TCE/raw/main/TExams/{image_filename}'
                keywords = match.iloc[0]['TEXT']
                st.markdown(f"**🌷 Keywords:** 🔑 {keywords}")
                st.image(image_url, caption=f'Exam Image for {selected_year}', width=800)
            else:
                st.write("No keywords or image found for this year.")

