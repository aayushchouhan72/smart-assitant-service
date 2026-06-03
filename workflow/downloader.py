from langchain.tools import tool
import yt_dlp as yt

@tool
def download_reel(url:str)->str:
    """Download video from instagram and return local path"""
    output ="temp_videos/video.mp4"

    option={
        "outtmpl":output
    }

    with yt.YoutubeDL(option) as ydl:
        ydl.download([url])

    
    return output
