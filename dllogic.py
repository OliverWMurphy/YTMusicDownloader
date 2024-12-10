import os
import subprocess
import asyncio
from pytubefix import YouTube as YT, Playlist as PL
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse



def single(URI: str)  -> str:  
    video = YT(URI)
    
    audio = video.streams.get_audio_only()
    if audio is None:
        raise Exception
    try:
        audio.download()
        print("Download Successful!")
    except Exception:
        print("Could get audio stream, but download failed")
        raise Exception
    
    return audio.default_filename

def playlist(URI: str, name: str) -> bool:
    playlist = PL(URI)
    
    for URI in playlist.video_urls:
        single(URI)
    return True

def id_to_URI(vid_id: str)-> str:
    return "https://www.youtube.com/watch?v=" + vid_id

def download_mp3(file_path,new_name):
    if not os.path.exists(file_path):
        return {"error": "File not found",
                "filePath": file_path}
    
    subprocess.run([
    'ffmpeg',
    '-i', os.path.join(file_path),
    os.path.join(new_name)
])


    # Use FileResponse to return the file, with headers to prompt download
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=new_name  # This sets the name of the file for download
    )

async def delete_file(file_path: str):
    """Delete the file after a 10-minute delay."""
    try:
        
        if os.path.exists(file_path):
            await asyncio.sleep(30)
            os.remove(file_path)
        else:
            pass
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
