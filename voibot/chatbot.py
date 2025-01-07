import os
import tempfile
import requests
import warnings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import AIMessage, HumanMessage

from .utils import download_pdf_from_url, prompt_func, openaiAPI, openaiReply

warnings.filterwarnings("ignore")

class VoiAssistant:
    def __init__(self, openai_key, pdf_urls, role, intents, replies, segment_assignments, dont_know_response=None):
        self.openai_key = openai_key
        os.environ['OPENAI_API_KEY'] = self.openai_key
        self.pdf_urls = pdf_urls if isinstance(pdf_urls, dict) else {"unified": pdf_urls if isinstance(pdf_urls, list) else [pdf_urls]}
        self.role = role
        self.intents = intents
        self.replies = replies
        self.segment_assignments = segment_assignments
        self.dont_know_response = dont_know_response if dont_know_response else {}  # Custom responses from the user
        self.indices = {}
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True) 

    def get_most_recent_response(self):
        """
        Returns the most recent response from the conversation history.
        """
        chat_history = self.memory.load_memory_variables({})

        # Ensure the chat_history is not empty
        if chat_history and chat_history.get("chat_history"):
            # Loop through the chat history in reverse to find the most recent assistant response
            for message in reversed(chat_history["chat_history"]):
                if isinstance(message, AIMessage):  
                    return message.content  
        return "Error: Most recent response could not be retrieved"
    
    def get_most_recent_query(self):
        """
        Returns the most recent query from the conversation history.
        """
        chat_history = self.memory.load_memory_variables({})
        
        if chat_history and chat_history.get("chat_history"):
            # Loop through the chat history in reverse to find the most recent assistant response
            for message in reversed(chat_history["chat_history"]):
                if isinstance(message, HumanMessage):  
                    return message.content  
        return "Error: Most recent query could not be retrieved"

    def initialize_assistant(self):
        try:
            embeddings = OpenAIEmbeddings()
            for segment, urls in self.pdf_urls.items():
                all_docs = []
                for pdf_url in urls:
                    # Download the PDF
                    downloaded_pdf_path = download_pdf_from_url(pdf_url)
                    loader = PyPDFLoader(downloaded_pdf_path)
                    documents = loader.load()

                    # Split the document text (fixed length overlapping split for accuracy)
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    docs = text_splitter.split_documents(documents)
                    all_docs.extend(docs)

                    os.remove(downloaded_pdf_path)

                # Create Chroma vectorstore for this segment
                self.indices[segment] = Chroma.from_documents(all_docs, embeddings)

            print(f"Assistant initialized with {len(self.indices)} segments: {', '.join(self.indices.keys())}")
        except Exception as e:
            print(f"Error initializing assistant: {str(e)}")

    def get_response(self, query):
        if not self.indices:
            raise ValueError("Assistant is not initialized.")

        # Construct the classification prompt
        prompt = prompt_func(query, 1, self.role, self.intents)

        category = openaiAPI(prompt, 0.5, self.openai_key)

        if category in self.intents:
            if self.replies.get(category) == "RAG":
                # Determine the appropriate segment (intent)
                segment = self.segment_assignments.get(category, "unified")
                if segment not in self.indices:
                    return f"Error: No database found for segment '{segment}'"

                # Perform retrieval with context memory
                retriever = self.indices[segment].as_retriever()
                conversational_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=retriever,
                    memory=self.memory 
                )
                result = conversational_chain.run({"question": query, "chat_history": self.memory.load_memory_variables({})})

                if result in ("I don't know", "I don't know."):
                    result = self.dont_know_response
            elif self.replies.get(category) == "role_based_llm_reply":
                # Use LLM to provide an appropriate role-based reply
                result = openaiReply(query, 0.9, category, self.openai_key, self.role)
            else:
                result = self.replies.get(category, "I'm not sure how to respond to that.")
                if "{most_recent_response}" in result:
                    previous_response = self.get_most_recent_response()
                    result = result.replace("{most_recent_response}", previous_response)
                elif "{most_recent_query}" in result:
                    previous_query = self.get_most_recent_query()
                    result = result.replace("{most_recent_query}", previous_query)
        else:
            result = "Unfortunately, I am unable to help you with that."

        # Save the chat history for context in future queries
        self.memory.save_context({"question": query}, {"response": result})

        return result
