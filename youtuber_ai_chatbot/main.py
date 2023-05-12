import streamlit as st
import textwrap
from streamlit_elements import elements, media
from chatbot import YouTubeChatbot
from components.sidebar import sidebar

def index():
    def put_media_player():
        with elements("media_player"):
            video_url = st.session_state.get("video_url")
            media.Player(url=video_url, controls=True)

    st.set_page_config(page_title="YoutuberGPT", page_icon="🤖", layout="wide")
    st.header("🤖YoutuberGPT")


    sidebar()
    video_url = st.text_input("YouTube Video Url:", on_change=put_media_player())

    session_state = st.session_state
    session_state["video_url"] = video_url
    question = st.text_area("Question:")


    if st.button("Ask any question related to the video"):
        with st.spinner('preparing answer'):
            chatbot = YouTubeChatbot()
            db = chatbot.create_db_from_youtube_video_url(video_url)
            answer = chatbot.get_response_from_query(db, question)
            st.subheader("Answer:")
            st.write(textwrap.fill(answer, width=50))

index()
