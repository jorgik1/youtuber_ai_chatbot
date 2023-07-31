# Temporary fix for pydantic issue @see https://github.com/streamlit/streamlit/issues/3218
import pydantic
pydantic.class_validators._FUNCS.clear()
import streamlit as st
from streamlit_elements import elements, media
from chatbot import YouTubeChatbot
from components.sidebar import sidebar
from langchain.memory import ConversationBufferWindowMemory
from streamlit_chat import message


def index():

    def put_media_player():
        with elements("media_player"):
            video_url = st.session_state.get('video_url')
            media.Player(url=video_url, controls=True)

    def clear_submit():
        st.session_state["submit"] = False

    st.set_page_config(page_title="YoutuberGPT", page_icon="🤖", layout="wide")
    st.header("🤖YoutuberGPT")
    sidebar()

    if 'responses' not in st.session_state:
        st.session_state['responses'] = [
            "Ask any question related to the video"
        ]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    if 'buffer_memory' not in st.session_state:
        st.session_state.buffer_memory = ConversationBufferWindowMemory(
            k=3, return_messages=True)

    if 'video_url' not in st.session_state:
        st.session_state['video_url'] = []

    if 'db' not in st.session_state:
        st.session_state['db'] = None

    videocontainer = st.container()
    # container for chat history
    response_container = st.container()
    # container for text box
    textcontainer = st.container()

    with videocontainer:
        video_url = st.text_input("YouTube Video Url:", on_change=clear_submit)
        if video_url != st.session_state['video_url']:
            st.session_state['video_url'] = video_url
            if video_url:
                put_media_player()

                chatbot = YouTubeChatbot()
                db = chatbot.create_db_from_youtube_video_url(video_url)
                if db is None:
                    st.session_state['db'] = None
                    return st.error("There is no transcript")
                st.session_state['db'] = db

    with textcontainer:
        question = st.text_area("Question:", key="question")
        if st.button("Run") or st.session_state.get("submit"):
            if st.session_state['db'] is not None:
                try:
                    with st.spinner('preparing answer'):
                        chatbot = YouTubeChatbot()
                        response = chatbot.get_response_from_query(
                            st.session_state['db'], question)
                        if response is None:
                            return st.error(
                                "There is no answer or something went wrong")
                        else:
                            st.session_state.requests.append(question)
                            st.session_state.responses.append(response)
                            st.session_state["submit"] = True
                except:
                    return st.error(
                        "There is no answer or something went wrong")

    with response_container:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i], key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i],
                            is_user=True,
                            key=str(i) + '_user')


index()
