youtuber_ai_chatbot
===================

Accurate Answers for YouTube Videos

Overview
--------
youtuber_ai_chatbot is a Python package that utilizes artificial intelligence to provide accurate answers for YouTube videos. It leverages natural language processing techniques to analyze video transcripts and generate responses to user queries.

Features
--------
- Extracts and processes YouTube video transcripts
- Generates accurate answers to user queries
- Supports multiple languages for transcript analysis
- Integrates with Streamlit for easy deployment and interaction

Installation
------------
To install youtuber_ai_chatbot, use pip:

.. code-block:: bash

    pip install youtuber_ai_chatbot

Usage
-----
Once installed, you can import the package and use it in your Python code:

.. code-block:: python

    from youtuber_ai_chatbot import YouTubeChatbot

    # Create a chatbot instance
    chatbot = YouTubeChatbot()

    # Create a database from a YouTube video URL
    video_url = "https://www.youtube.com/watch?v=<video_id>"
    db = chatbot.create_db_from_youtube_video_url(video_url)

    # Get a response for a user query
    question = "What is the main topic of the video?"
    response = chatbot.get_response_from_query(db, question)

    print(response)

Contributing
------------
Contributions are welcome! If you have any bug reports, feature requests, or suggestions, please open an issue on the project's GitHub repository.

License
-------
This project is licensed under the MIT License. See the `LICENSE` file for more information.

