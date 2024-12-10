
import dllogic
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
@app.get("/api/single/{vid_id}")
async def download_single(vid_id: str, splitTracksFromDesc: bool = False):
    print("STARTING")
    URL = dllogic.id_to_URI(vid_id)
    print(f"Obtained URL: {URL}")

    result = await dllogic.single(URL, splitTracksFromDesc)
    print(result)

    if result == "":
        raise HTTPException(status_code=400, detail = "Error processing video")
        
    new_name = result[:-4] + ".mp3"
    background_tasks.add_task(dllogic.delete_file, result)

    return dllogic.download_mp3(result, new_name)

#
# Tutorial stuff here
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item