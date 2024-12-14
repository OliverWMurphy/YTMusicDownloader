
import os
import dllogic
import utils
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

background_tasks = BackgroundTasks()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins, change to specific origins for security (e.g., ["http://localhost:5500"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#splitTracks: Union[bool, None]
@app.get("/api/single/{videoId}")
async def download_single(videoId: str, splitTracksFromChapters: bool = False):
    
    utils.ForceMakeEmptyDir(videoId)
    print("STARTING")
    URL = dllogic.id_to_URL(videoId)
    print(f"Obtained URL: {URL}")
    video = await dllogic.getVideo(URL)
    audioName = await dllogic.getAudio(video,videoId)
    print(audioName)
    targetLocation = dllogic.create_mp3(audioName,videoId)
    
    if splitTracksFromChapters:
        print("Splitting")
        chapters = video.chapters
        targetLocation = dllogic.splitAudio(targetLocation,chapters)
    
    background_tasks.add_task(dllogic.delete_file, audioName)
    
    print("About to download")
    # Use FileResponse to return the file, with headers to prompt download
    return FileResponse(
        path=targetLocation,
        media_type="video/mp4",
        filename=targetLocation,  # This sets the name of the file for download
    )