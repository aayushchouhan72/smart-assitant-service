import os
import cv2
import base64
from groq import Groq
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@tool
def analyze_video(video_path:str)->str:
    """Analyze video context."""

    cap = cv2.VideoCapture(video_path)

    success, frame = cap.read()

    if not success:
        return "Cannot read video."

    frame_path="frame.jpg"

    cv2.imwrite(
        frame_path,
        frame
    )

    with open(frame_path,"rb") as f:
        image=base64.b64encode(
            f.read()
        ).decode()

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role":"user",
                "content":[
                    {
                        "type":"text",
                        "text":"Analyze this video frame."
                    },
                    {
                        "type":"image_url",
                        "image_url":{
                            "url":f"data:image/jpeg;base64,{image}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

