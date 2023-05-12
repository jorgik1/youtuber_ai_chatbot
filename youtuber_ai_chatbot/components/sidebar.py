import streamlit as st
from components.faq import faq

def sidebar():
    with st.sidebar:
        st.markdown("YoutuberGPT")
        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "YouTuberGPT allows you to ask questions about YouTube videos. "
        )
        faq()
        st.markdown(
            "This tool is a work in progress. "
            "You can contribute to the project on [GitHub](https://github.com/jorgik1/youtuber_ai_chatbot) "  # noqa: E501
            "with your feedback and suggestions💡"
        )
        st.markdown("Made by [jorgik1](https://github.com/jorgik1)")
        st.markdown("---")
        st.markdown("# Donate")
        st.markdown("[Buy me a coffee](https://www.buymeacoffee.com/youtubergtp)")
