
import os

from workflow.downloader import download_reel
from workflow.analyzer import analyze_video
from workflow.caption_agent import generate_caption
from workflow.editor import edit_video
from workflow.email_sender import send_email
from workflow.cleanup import cleanup
from workflow.cloudinary_upload import upload_video


def run_workflow(
    url:str,
    receiver_email:str
):

    try:

        print("\nDownloading video...")

        video_path = download_reel.invoke(
            {
                "url":url
            }
        )

        print(
            f"Downloaded: {video_path}"
        )



        print("\nAnalyzing video...")

        analysis = analyze_video.invoke(
            {
                "video_path":video_path
            }
        )

        print(
            f"\nAnalysis:\n{analysis}"
        )



        print(
            "\nGenerating caption..."
        )

        caption = generate_caption.invoke(
            {
                "video_context":analysis
            }
        )

        print(
            f"\nCaption:\n{caption}"
        )



        print(
            "\nEditing video..."
        )

        edited_video = edit_video.invoke(
            {
                "video_path":video_path
            }
        )

        print(
            f"Edited: {edited_video}"
        )

        print("Video is uploaded to cloudinary...")
        video_url = upload_video.invoke({"video_path": edited_video})

        print("Video is uploaded to Cloudinary")
       
       

        print(
            "\nSending email..."
        )

        email_result = send_email.invoke(
            {
                "receiver_email":
                receiver_email,

                "video_path":
                edited_video,

                "caption":
                caption
            }
        )

        print(email_result)



    finally:

        print(
            "\nCleaning temp files..."
        )

        cleanup.invoke(
            {
                "file_paths":[
                    video_path,
                    edited_video,
                    "frame.jpg"
                
                ]
            }
        )

        print(
            "Cleanup completed."
        )


if __name__=="__main__":

    run_workflow(

        url="https://www.instagram.com/reel/DZEziavAfpX/?igsh=MWw0NWgycHUxOG8wcA==",

        receiver_email=
        "aayushchouhanxyz27@gmail.com"
    )