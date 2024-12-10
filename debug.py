from pytubefix import YouTube as YT, Playlist as PL
from dllogic import single

video = YT(r"https://www.youtube.com/watch?v=1bsFH6t8eFw")
audio = video.streams.get_audio_only()
if audio is None:
    raise Exception
try:
    audio.download()
    print("Download Successful!")
except Exception:
    print("Could get audio stream, but download failed")
    raise Exception
