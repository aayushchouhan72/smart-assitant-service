import os 
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain.tools import tool
from rich import print
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

#  Get llm model
def get_llm():
    return ChatMistralAI(
        model="mistral-large-latest",
        api_key=os.getenv("MISTRAL_API_KEY")
        )

#  Chat prompt template 
prompt = ChatPromptTemplate.from_messages(
        [
            ("system","""
You are an expert social media content creator.

Based on the video context below generate:

1. Viral Caption
2. 10 Relevant Hashtags
3. Content Category
4. Content Tone
             
only return caption with hastages(caption should accoring to toon of video and it should be 40-50 characters)
dont write heading caption and hastage 
"""),
    ("human","""
this is the given context of video on this basis of it genrate mention things  
     video context :
     {video_context}

""")
        ]
    )

@tool
def generate_caption(video_context:str)->str:
    """Gentare caption and viral hastages for the reel"""
    llm= get_llm()
    
    final_prompt=prompt.format_messages(
        video_context=video_context
    )

    response=  llm.invoke(final_prompt)

    return response.content



    

