from chatbot import YouTubeChatbot
import streamlit as st
import textwrap


st.set_page_config(page_title="Youtuber Chatbot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

def index():
    st.title("Youtuber AI Chatbot")

    video_url = st.text_input("YouTube Video Url:")
    question = st.text_area("Question:")

    if st.button("Ask any question relate to the video"):
        chatbot = YouTubeChatbot()
        db = chatbot.create_db_from_youtube_video_url(video_url)
        answer = chatbot.get_response_from_query(db, question)
        st.subheader("Answer:")
        st.write(textwrap.fill(answer, width=50))
index()
