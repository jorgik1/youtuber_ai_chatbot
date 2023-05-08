# Project Description
This is a YouTube chatbot that uses OpenAI's GPT-3 language model to generate conversational responses. The chatbot is trained on the transcripts of a YouTuber's videos and can provide conversational responses to user's queries.

# Installation and Usage
## Clone the Repository
```
git clone https://github.com/jorgik1/youtuber_ai_chatbot.git
cd youtuber_ai_chatbot
```
## Install Required Libraries
```
pip install -r requirements.txt
```
## Set Your OpenAI API Key
Create a file named .env and copy the contents of .env.example into it. Then replace <your_api_key> with your OpenAI API key.
```
cp .env.example .env
```
OPENAI_API_KEY=<your_api_key>

## Start the Chatbot
```
python main.py
```

## Usage
1. Enter the video ID of the YouTuber you want to chat with, e.g. dQw4w9WgXcQ.
2. Enter your name or a nickname to use in the chat.
3. Enter your first message/question to start the conversation.
4. The chatbot will respond with an answer. Continue the conversation by entering your next question or message.
5. To end the chat, enter exit.
