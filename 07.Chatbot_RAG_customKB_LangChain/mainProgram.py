import os
from dotenv import load_dotenv
from colorama import Fore

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Prompt Template below
template = """
You are a customer support specialist.
Use the following context to answer the question.

Context:
{context}

Question:
{question}
"""

chat_prompt_template = ChatPromptTemplate.from_template(template)

# Model selection - Selected cheaper one for testing purpose
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.9
)

# Helper function definition 
def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


# Load & Split FAQ file - KnowledgeBase document
def load_documents():
    raw_documents = TextLoader("./docs/knolwledgeBase.txt").load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    #print(str(text_splitter))
    #print(str(text_splitter.split_documents(raw_documents)))
    return text_splitter.split_documents(raw_documents)

# Create Vector Store
def load_embeddings(documents):
    db = Chroma.from_documents(
        documents,
        OpenAIEmbeddings()
    )
    return db.as_retriever()


# Generate Response (RAG Chain)
def generate_response(retriever, query):
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | chat_prompt_template
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)


# Query Entry Point
def query(user_query):
    documents = load_documents()
    retriever = load_embeddings(documents)
    response = generate_response(retriever, user_query)
    return response


# If you want - CLI Run can be used
if __name__ == "__main__":
    while True:
        user_input = input(Fore.GREEN + "You: ")

        if user_input.lower() == "exit":
            break

        answer = query(user_input)
        print(Fore.CYAN + "Bot:", answer)