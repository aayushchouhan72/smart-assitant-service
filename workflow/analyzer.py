
import time
from google import genai
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

# Initialize the client (Make sure GEMINI_API_KEY is set in your environment variables)
client = genai.Client()


@tool
def analyze_video(video_path:str)->str:
    """Analyze video context.""" 
    print("Uploading video file...")
  

    video_file = client.files.upload(file=video_path)
    print(f"Uploaded successfully. File URI: {video_file.uri}")
    
    while video_file.state.name == "PROCESSING":
        print("Waiting for video processing...")
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)
    
    if video_file.state.name == "FAILED":
        raise ValueError(f"Video processing failed: {video_file.error.message}")
    
    print("Analyzing video...")
    # Step 3: Send the file URI to the model for analysis
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # High-speed, low-cost model perfect for automations
        contents=[
            video_file, 
            "Provide a detailed summary of what happens in this video. Provide timestamps for key events."
        ]
    )
    
    print("\n--- Analysis Result ---")
    print(response.text)
    
    # Optional Step 4: Clean up the file from Gemini storage if needed
    client.files.delete(name=video_file.name)

    return response.text