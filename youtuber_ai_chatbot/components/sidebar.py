import streamlit as st
from components.faq import faq

def sidebar():
    with st.sidebar:
        st.markdown("# 🤖YoutuberGPT")
        st.markdown("---")
        st.markdown("# How to use?")
        st.markdown(
            "- Input the URL of the video you are interested in "
            "- YouTuberGPT will use its advanced semantic search "
            "capabilities to analyze the video and generate accurate and helpful answer to your questions ")

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
