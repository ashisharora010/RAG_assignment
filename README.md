# RAG_assignment



# ChatBot using RAG

Retrieval Augmented Generation is a great technique that combines the strengths of language
models like GPT-3 with the power of information retrieval. By enriching the input with
context-specific information, RAG enables language models to generate more accurate and
contextually relevant responses.

## Input Based Implementation:

    1. Please provide the OPENAI_KEY in the program.
    2. Run ‘python3 run_text.py’
    3. Once the DB is created, a user can start asking queries with respect to the given
    knowledge document.
    4. If a user wants to close the session, typing ‘resolved’ will close the session.


## Audio Based Implementation:

    1. Please provide the OPENAI_KEY and ASSEMBLYAI_KEY in the program.
    2. Run ‘python3 run_audio.py’
    3. Once the DB is created, a user needs to wait for 5 seconds.
    5. After 5 seconds, it will start recording the query for the next 10 seconds.
    6. It will hit the OPENAI server automatically and return the response to the program.
    7. Automatically, the text will be processed in a form of audio and played out loud from the
    machine.
    8. Again from point 5, a user can put up a new query in the same session.
