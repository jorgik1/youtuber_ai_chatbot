from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate)


        # Human question prompt
human_template = "Answer the following question: {question}"
HUMAN_PROMPT = HumanMessagePromptTemplate.from_template(human_template)
        # Template to use for the system message prompt
template = """
  You are a helpful assistant that that can answer questions about youtube videos
  based on the video's transcript: {docs}

  Only use the factual information from the transcript to answer the question.

  If you feel like you don't have enough information to answer the question, say "I don't know".

  Your answers should be verbose and detailed.
  """

PROMPT_TEMPLATE = SystemMessagePromptTemplate.from_template(template)


CHAT_PROMPT = ChatPromptTemplate.from_messages([PROMPT_TEMPLATE, HUMAN_PROMPT])
