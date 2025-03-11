import streamlit as st
import pandas as pd

# Define tab navigation
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
            matches = df[df['YEAR'].str.startswith(query.strip()[:4])]
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

    # Streamlit layout for search
    st.markdown('#### Teacher Certificate Exam Searching Engine')
    st.subheader('❄️ [1] Search Data')

    search_mode = st.radio("Search Mode", ["Search questions by YEAR", "Search questions by Keywords", "Search questions by Words"])
    query = st.text_input("Search Query: e.g., 2024 (by YEAR) or tapping (by Keywords or Words)", "")
    search_button = st.button('Click to Search')

    if search_button:
        results = search_years(search_mode, query)
        if results:
            st.session_state['results'] = results
            st.session_state['selected_year'] = results[0]  # Default to first result
            st.write("Search completed successfully.")

    # Select box to choose year from results
    if 'results' in st.session_state:
        selected_year = st.selectbox("Select a year from the results", st.session_state['results'], index=0, key='selected_year')

    # Button to display exam question
    if st.button('Show me the exam question') and 'selected_year' in st.session_state:
        match = df[df['YEAR'] == st.session_state['selected_year']]
        if not match.empty:
            image_filename = match.iloc[0]['Filename']
            image_url = f'https://huggingface.co/spaces/MK-316/TCE/raw/main/TExams/{image_filename}'
            keywords = match.iloc[0]['TEXT']
            st.markdown(f"**🌷 Keywords:** 🔑 {keywords}")
            st.image(image_url, caption=f'Exam Image for {st.session_state['selected_year']}', width=800)
        else:
            st.write("No keywords or image found for this year.")
