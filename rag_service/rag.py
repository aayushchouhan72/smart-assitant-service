from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv

load_dotenv()

#  Embedding model 
def get_embeding_model():
    return MistralAIEmbeddings()

#  LLM model
def get_llm_model():
    return ChatMistralAI(model_name="mistral-small-2506")

# Create vectore db
def  create_db(text:str)->Chroma:
    splitter =RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks= splitter.create_documents([text])

    embedding_model=get_embeding_model()
    vectorestore=Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )
    return vectorestore

#  Create Related context for model 
def get_context(query:str,text:str)->dict:
    vectorestore=create_db(text)
    retriver = vectorestore.as_retriever(
        search_type='mmr',
        search_kwargs = {
        "k" : 4,
        "fetch_k":10,
        "lambda_mult" :0.5
    }
  
    )
    docs=  retriver.invoke(query)
    return {
        "query":query,
        "docs":docs
    }

# LLM Serch 
def llm_search(query:dict)->str:
    context = "\n\n".join(doc.page_content for doc in query['docs'])
    question = query['query']

    llm = get_llm_model()

    prompt= ChatPromptTemplate.from_messages([
        ("system","""
You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
         """),
         ("human","""
Context:
{context}

Question:
{question}

""")
    ])

    final_prompt = prompt.invoke({
        "context" :context,
        "question": question
    })
    
    response  =  llm.invoke(final_prompt)
    return response



