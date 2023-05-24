from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate)

# Human question prompt
human_template = "Answer the following question: {question}"
HUMAN_PROMPT = HumanMessagePromptTemplate.from_template(human_template)

# Template to use for the system message prompt
template = """
You are a helpful assistant that can answer questions about YouTube videos based on their transcripts.

To provide accurate answers, please refer to the factual information in the video transcript: {docs}

If you don't have enough information to answer the question, please respond with "I don't know".

Your answers should be detailed and provide as much information as possible.
"""

PROMPT_TEMPLATE = SystemMessagePromptTemplate.from_template(template)

CHAT_PROMPT = ChatPromptTemplate.from_messages([PROMPT_TEMPLATE, HUMAN_PROMPT])
