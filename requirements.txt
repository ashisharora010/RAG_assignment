import os
import openai
import tiktoken
import chromadb

from langchain.document_loaders import OnlinePDFLoader, UnstructuredPDFLoader, PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai_key="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"


def creating_DB(document):
    '''
        def: this function is responsible to create the vector DB for the knowldge document. 
        args:
          document: .pdf document
        return:
          vectorDB: vector DB for the .pdf docoument
    '''
    loader = PyPDFLoader(document)
    pdfData = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splitData = text_splitter.split_documents(pdfData)

    collection_name = "pan_card"
    local_directory = "pan_card_embedding"
    persist_directory = os.path.join(os.getcwd(), local_directory)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    ## Creating the vector DB
    vectDB = Chroma.from_documents(splitData,
                        embeddings,
                        collection_name=collection_name,
                        persist_directory=persist_directory
                        )
    ## Storing the vector DB
    vectDB.persist()
    return vectDB





def run(document):
    '''
        def: this function is responsible to create a chatBot using GPT-3.5-turbo and takes query as a real time input unless you close the session.
        args:
          document: .pdf document
    '''
    vectDB = creating_DB(document)
    # We are using a MultiQueryRetriever to get the same context from different sentences
    retriever_from_llm = MultiQueryRetriever.from_llm(retriever=vectDB.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.2}),
                                                    llm=ChatOpenAI(openai_api_key=openai_key,temperature=0))

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # Creating the chatbot
    chatQA = ConversationalRetrievalChain.from_llm(
                OpenAI(openai_api_key=openai_key,
                temperature=0.2, model_name="gpt-3.5-turbo"), 
                retriever_from_llm, 
                memory=memory)
    ## initialzing the chat history
    chat_history = []
    
    query = ""
    while query != 'resolved':
        print("chat_history", chat_history)
        query = input('Question: ')
        if query != exit:
            response = chatQA({"question": query, "chat_history": chat_history})
            print('answer',response["answer"])
            chat_history.append((query, response["answer"]))
    return 

if __name__ == "__main__":
    run("graph.pdf")

