import streamlit as st
import os
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from prompts import CHAT_PROMPT
from youtube_transcript_api import NoTranscriptFound

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class YouTubeChatbot:

    def __init__(self):
        load_dotenv(find_dotenv())

        if (st.secrets.hugging_face_api_key is not None):
            os.environ.setdefault("HUGGINGFACEHUB_API_TOKEN",
                                  st.secrets.hugging_face_api_key)
        if (st.secrets.open_ai_key is not None):
            os.environ.setdefault("OPENAI_API_KEY", st.secrets.open_ai_key)

        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name='all-MiniLM-L6-v2')
        except Exception as e:
            st.error("Failed to load the Hugging Face Embeddings model: " +
                     str(e))
            self.embeddings = None

        try:

            self.model = ChatOpenAI()

        except Exception as e:
            st.error("Failed to load the LLM model: " + str(e))
            self.model = None


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

        if _self.model is None:
            st.error(
                "LLM model is not loaded. Please check the error messages."
            )
            return None

        docs = _db.similarity_search(query, k=k)
        docs_page_content = " ".join([d.page_content for d in docs])

        try:
            chain = LLMChain(llm=_self.model, prompt=CHAT_PROMPT)
            response = chain.run(
                question=query,
                docs=docs_page_content,
                verbose=True,
                memory=st.session_state.buffer_memory,
            )
            response = response.replace("\n", "")
            return response
        except Exception as e:
            st.error("Failed to generate a response: " + str(e))
            return None
