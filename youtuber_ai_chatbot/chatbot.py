from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from prompts import CHAT_PROMPT
from youtube_transcript_api import NoTranscriptFound
import streamlit as st
import os


class YouTubeChatbot:

    def __init__(self):
        load_dotenv(find_dotenv())

        if (st.secrets.hugging_face_api_key is not None):
            os.environ.setdefault("HUGGINGFACEHUB_API_TOKEN",
                                  st.secrets.hugging_face_api_key)

        try:
            self.embeddings = HuggingFaceEmbeddings()
        except Exception as e:
            st.error("Failed to load the Hugging Face Embeddings model: " +
                     str(e))
            self.embeddings = None

        try:
            repo_id = "tiiuae/falcon-7b-instruct"
            self.falcon_llm = HuggingFaceHub(
                repo_id=repo_id, model_kwargs={"temperature": 0.1, "max_new_tokens": 500}
            )

        except Exception as e:
            st.error("Failed to load the Falcon LLM model: " + str(e))
            self.falcon_llm = None


    @st.cache_data
    def create_db_from_youtube_video_url(_self, video_url):
        st.info("Creating FAISS database from YouTube video.")
        loader = YoutubeLoader.from_youtube_url(video_url)
        try:
            transcript = loader.load()
        except NoTranscriptFound:
            st.error("No transcript found for the video.")
            return None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                       chunk_overlap=100)
        docs = text_splitter.split_documents(transcript)
        st.info("Number of documents: " + str(len(docs)))

        try:
            db = FAISS.from_documents(docs, _self.embeddings)
            st.text("Created FAISS database from documents.")
            return db
        except Exception as e:
            st.error("Failed to create FAISS database from documents: " +
                     str(e))
            return None

    @st.cache_data
    def get_response_from_query(_self, _db, query, k=4):
        if _db is None:
            st.error(
                "Database is not initialized. Please check the error messages."
            )
            return None

        if _self.falcon_llm is None:
            st.error(
                "Falcon LLM model is not loaded. Please check the error messages."
            )
            return None

        docs = _db.similarity_search(query, k=k)
        docs_page_content = " ".join([d.page_content for d in docs])

        try:
            chain = LLMChain(llm=_self.falcon_llm, prompt=CHAT_PROMPT)
            response = chain.run(
                question=query,
                docs=docs_page_content
            )
            response = response.replace("\n", "")
            return response
        except Exception as e:
            st.error("Failed to generate a response: " + str(e))
            return None
