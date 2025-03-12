import streamlit as st

def phonetics_apps_page():
    st.markdown('### 🐾 Distinctive feature Practice Apps')
    st.write('Applications to train yourself with distinctive features in phonology')

    # Describing your apps briefly
    st.caption("""
    Here is a selection of applications designed to enhance feature matrix learning through interactive and innovative tools.
    """)

    # First row with three columns
    col1, col2, col3 = st.columns(3)  # Define columns for the first row

    with col1:
        st.image("images/button01.png", width=100)
        if st.button('App 1: Distinctive features', key='3'):
            st.markdown("🌀[App link](https://mk-316-featureapp01.hf.space/): Phonology, Sound grouping from distinctive features", unsafe_allow_html=True)
            st.markdown("2024.10.15")
    with col2:
        st.image("images/button01.png", width=100)
        if st.button('App 2: Feature Quiz 1', key='5'):
            st.markdown("🌀[App link](https://mk-316-feature-practice.hf.space/): Phonology, Distinctive feature quiz (click)", unsafe_allow_html=True)
            st.markdown("2024.10.14")
    with col3:
        st.image("images/button01.png", width=100)
        if st.button('App 3: Feature Quiz 2', key='6'):
            st.markdown("🌀[App link](https://feature-quiz02.streamlit.app/): Phonology, Distinctive feature quiz (choose)", unsafe_allow_html=True)
            st.markdown("2024.11.6")   
    # Add some space before the second row
    st.write("\n\n")


phonetics_apps_page()

# URL to the raw image on GitHub
image_url = "https://github.com/MK316/MK-316/raw/main/images/bg2.png"
# Display the image
st.image(image_url, caption="\"He who knows no foreign languages knows nothing of his own.\" — Johann Wolfgang von Goethe", use_container_width=True)
