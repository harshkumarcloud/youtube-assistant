import os
import streamlit as st
from dotenv import load_dotenv
import langchain_helper as lch

load_dotenv()

st.set_page_config(page_title="YouTube Assistant", layout="wide")
st.title("YouTube Assistant")

with st.sidebar:
    with st.form(key="my_form"):
        youtube_url = st.text_input(
            label="What is the YouTube video URL?",
            placeholder="https://www.youtube.com/watch?v=...",
        )
        query = st.text_area(
            label="Ask me about the video:",
            max_chars=200,
            key="query",
        )
        submit_button = st.form_submit_button(label="Submit")

if submit_button:
    # Check if the Google API key exists in your .env file
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Google API key missing! Please add GOOGLE_API_KEY to your .env file.")
        st.stop()

    if not youtube_url or not query:
        st.warning("Please provide both a YouTube URL and a question.")
        st.stop()

    with st.spinner("Processing video transcript and generating response..."):
        try:
            db = lch.create_db_from_youtube_video_url(youtube_url)
            response, docs = lch.get_response_from_query(db, query)

            st.subheader("Answer:")
            st.write(response)

            with st.expander("Show relevant transcript snippets"):
                for idx, doc in enumerate(docs, start=1):
                    st.markdown(f"**Chunk {idx}:**")
                    st.write(doc.page_content)
        except Exception as e:
            st.error(f"An error occurred: {e}")