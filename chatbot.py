import pickle

from langchain.text_splitter import CharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.prompts import PromptTemplate
from transformers import LongformerTokenizer


class YoutuberAIChatbot:
    def __init__(self, qa, youtuber_name):
        self.qa = qa
        self.youtuber_name = youtuber_name
        self.tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')

    def _truncate_chat_history(self, chat_history, max_tokens):
        if len(chat_history) == 0:
            return []

        total_tokens = sum([len(self.tokenizer.encode(dialogue_turn)) for dialogue_turn in chat_history])
        if total_tokens <= max_tokens:
            return chat_history

        truncated_chat_history = []
        remaining_tokens = max_tokens

        for dialogue_turn in reversed(chat_history):
            dialogue_tokens = self.tokenizer.encode(dialogue_turn)
            if len(dialogue_tokens) <= remaining_tokens:
                truncated_chat_history.insert(0, dialogue_turn)
                remaining_tokens -= len(dialogue_tokens)
            else:
                break

        return truncated_chat_history

    def ask(self, question, youtuber_name=None, chat_history=None):
        if chat_history is None:
            chat_history = []

        if len(chat_history) > 0:
            max_tokens = 4096 - len(self.tokenizer.encode(question)) - sum(
                [len(self.tokenizer.encode(dialogue_turn)) for dialogue_turn in chat_history])
        else:
            max_tokens = 2000

        truncated_chat_history = self._truncate_chat_history(chat_history, max_tokens)

        result = self.qa({"name": youtuber_name, "question": question, "chat_history": truncated_chat_history},
                         return_only_outputs=True)
        return result["answer"]


def create_youtuber_chatbot(video_id, youtuber_name, openai_api_key):
    t = YouTubeTranscriptApi.get_transcript(video_id)
    final_string = " ".join(item["text"] for item in t)

    text_splitter = CharacterTextSplitter()
    chunks = text_splitter.split_text(final_string)

    vector_store = FAISS.from_texts(chunks, OpenAIEmbeddings(openai_api_key=openai_api_key))
    with open("vectors-store.pkl", "wb") as f:
        pickle.dump(vector_store, f)

    qa_prompt_template = """You are an AI version of the youtuber {name} in video ID {video_id}.
    You are given the following extracted parts of a document and a question. Provide a conversational answer.
    Question: {question}
    =========
    {context_start}
    {context_end}
    =========
    Answer:"""

    qa_prompt = PromptTemplate(template=qa_prompt_template,
                               input_variables=["name", "video_id", "question", "context_start", "context_end"])

    qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0, openai_api_key=openai_api_key),
                                    vectorstore=vector_store, condense_question_prompt=qa_prompt)

    return YoutuberAIChatbot(qa, youtuber_name)

