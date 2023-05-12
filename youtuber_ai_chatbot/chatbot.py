from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from prompts import CHAT_PROMPT
from openai.error import OpenAIError
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
        loader = YoutubeLoader.from_youtube_url(video_url)
        transcript = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(transcript)

        db = FAISS.from_documents(docs, _self.embeddings)
        return db

    @st.cache_data
    def get_response_from_query(_self, _db, query, k=4):
        """
        gpt-3.5-turbo can handle up to 4097 tokens. Setting the chunksize to 1000 and k to 4 maximizes
        the number of tokens to analyze.
        """
        docs = _db.similarity_search(query, k=k)
        docs_page_content = " ".join([d.page_content for d in docs])
        try:
            chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
            chain = LLMChain(llm=chat, prompt=CHAT_PROMPT)
            response = chain.run(question=query, docs=docs_page_content)
            response = response.replace("\n", "")
            return response
        except:
            OpenAIError()




