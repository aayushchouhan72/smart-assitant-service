import subprocess
from langchain.tools import tool


@tool
def edit_video(video_path:str)->str:
    """Edit video appearance."""

    output_path = "temp_videos/edited.mp4"

    command = [

        "ffmpeg",

        "-i",
        video_path,

        "-vf",

        "scale=720:1280,eq=brightness=0.05:contrast=1.2",

        "-y",

        output_path
    ]

    subprocess.run(
        command,
        check=True
    )

    return output_path
