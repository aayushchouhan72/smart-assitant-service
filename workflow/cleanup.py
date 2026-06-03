import os
from langchain.tools import tool


@tool
def cleanup(
    file_paths:list[str]
)->str:
    """Delete temporary workflow files."""

    deleted_files=[]

    for path in file_paths:

        if os.path.exists(path):

            os.remove(path)

            deleted_files.append(path)

    return f"Deleted: {deleted_files}"
