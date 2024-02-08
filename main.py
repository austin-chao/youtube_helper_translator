import langchain_helper_ytassistant as lch
import streamlit as st
import textwrap

st.title("Youtube Assistant")

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.sidebar.text_area(
            label = "What is the Youtube video URL?",
            max_chars = 50
        )
        query = st.sidebar.text_area(
            label = "Ask me about the video?",
            max_chars = 50,
            key = "query"
        )
        is_foreign_language = st.sidebar.toggle(
            label = "Is this spoken in a foreign language?",
            key = "is_foreign_language"
        )    

        submit_button = st.form_submit_button(
            label = "Submit"
        )

if query and youtube_url and submit_button == True:
    if is_foreign_language == True:
        db = lch.create_vector_db_from_youtube_audio(youtube_url)
    else:
        db = lch.create_vector_db_from_youtube_url(youtube_url)

    response = lch.get_response_from_query(db, query)
    #index_description = lch.get_index_description(db)

    st.subheader("Answer:")
    st.text(textwrap.fill(response,width=150))

    lch.clear_vector_db(db)

    #st.subheader("Index Status:")
    #st.text(textwrap.fill(index_description,width=80))