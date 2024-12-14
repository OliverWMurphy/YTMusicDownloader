import asyncio
import os
import subprocess
import shutil


from fastapi import BackgroundTasks
from fastapi.responses import FileResponse
from HiddenPrints import HiddenPrints
from pytubefix import YouTube as YT, Playlist as PL, Chapter
from typing import Union, List

async def getVideo(Url: str)  -> YT:  
    return YT(Url)

async def getAudio(video: YT, path: str)  -> str:  
    audio = video.streams.get_audio_only()
    if audio is None:
        raise Exception
    try:
        audio.download(path)
        print("Download Successful!")
    except Exception:
        print("Could get audio stream, but download failed")
        raise Exception
    
    return audio.default_filename

# async def playlist(Url: str, splitTracksFromChapters: List[bool]) -> bool:
#     playlist = PL(Url)
    
#     for i in range(len(playlist.video_urls)):
#         await getAudio(playlist.video_urls[i])
#     return True

def id_to_URL(vid_id: str)-> str:
    return "https://www.youtube.com/watch?v=" + vid_id

def create_mp3(audioName: str, fileDestination: str) -> str:
    if not os.path.exists(fileDestination):
        raise Exception

    fileName = os.path.splitext(audioName)[0]
    mp3File = fileName + ".mp3"
    print("Starting FFMPEG")
    print(f"{fileDestination}/{audioName} -> {fileDestination}/{mp3File}")

    subprocess.run(
        ["ffmpeg", "-i", os.path.join(fileDestination,audioName), os.path.join(fileDestination,mp3File)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    print("Ending FFMPEG")

    return os.path.join(fileDestination,mp3File)

def splitAudio(audioName: str, chapters: List[Chapter]) -> str:
    folderName = os.path.splitext(audioName)[0]
    folderExists = False
    print(folderName)
    while not folderExists:
        try:
            os.mkdir(folderName)
            folderExists = True
        except FileExistsError:
            folderName += "Copy"

    for chapter in chapters:
        name = f"{chapter.title}.mp3"
        startTime = f"{chapter.start_seconds}"
        duration = f"{chapter.duration}"
        
        ffmpeg = ["ffmpeg", "-ss", startTime, "-t", duration, "-i", audioName, f"{folderName}/{name}"]
        print(f"Running {ffmpeg}" )
        subprocess.run(
            ffmpeg,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        
    zipName = shutil.make_archive(folderName, 'zip', folderName)
    shutil.rmtree(folderName)
    return zipName    

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
