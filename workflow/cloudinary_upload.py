import os
import cloudinary
import cloudinary.uploader

from dotenv import load_dotenv
from langchain.tools import tool


load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@tool 
def upload_video(
    video_path:str
)->str:
    """Upload video to cloudinary"""
    result = cloudinary.uploader.upload_large(
        video_path,
        resource_type="video"
    )
    return result['secure_url']


