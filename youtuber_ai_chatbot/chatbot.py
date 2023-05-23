from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import LLMChain, OpenAI
from dotenv import find_dotenv, load_dotenv
from prompts import CHAT_PROMPT
from youtube_transcript_api import NoTranscriptFound
import streamlit as st
import os


if (st.secrets.openai_api_key is not None):
    os.environ.setdefault("OPENAI_API_KEY", st.secrets.openai_api_key),


class YouTubeChatbot:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

    @st.cache_data
    def create_db_from_youtube_video_url(_self, video_url):
        """
        A function that creates a database from a YouTube video URL. It takes in a video URL and uses a YoutubeLoader
        to load the transcript of the video. If there is no transcript, it raises a ValueError. It then splits the
        transcript into smaller chunks of 1000 characters with an overlap of 100, and uses FAISS to create a database
        of these chunks using the embeddings provided. Returns the created database.
        :param _self: The instance of the class calling the function.
        :param video_url: The URL of the YouTube video to create the database from.
        :return: The created database.
        """
        loader = YoutubeLoader.from_youtube_url(video_url)
        try:
            transcript = loader.load()
        except NoTranscriptFound:
            raise ValueError("No transcript found for the video.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(transcript)

        db = FAISS.from_documents(docs, _self.embeddings)
        return db

    @st.cache_data
    def get_response_from_query(_self, _db, query, k=4):
        """
        A function that returns a response from a query via a similarity search and
        OpenAI's text-davinci-003 model.

        :param _self: an instance of the class calling the function
        :param _db: a database object to perform similarity search
        :param query: a string query to search for
        :param k: an integer number of documents to return from similarity search (default=4)

        :return: a string response from OpenAI's text-davinci-003 model or None if an error occurs
        """
        docs = _db.similarity_search(query, k=k)
        docs_page_content = " ".join([d.page_content for d in docs])
        try:
            chat = OpenAI(model_name="text-davinci-003", temperature=0.2)
            chain = LLMChain(llm=chat, prompt=CHAT_PROMPT)
            response = chain.run(question=query, docs=docs_page_content)
            response = response.replace("\n", "")
            return response
        except:
            return None
