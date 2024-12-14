import os

def ForceMakeEmptyDir(dirPath: str) -> None:
    dirExists = os.path.isdir(dirPath)
    if dirExists:
        for f in os.listdir(dirPath):
            if not f.endswith((".zip",".mp3",".m4a")):
                continue
            os.remove(os.path.join(dirPath, f))        
    else:
        os.mkdir(dirPath)
