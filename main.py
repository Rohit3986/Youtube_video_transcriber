from fastapi import FastAPI
import youtube_transcript_api
from urllib.parse import urlparse, parse_qs
from pydantic import BaseModel
from youtube_transcript_api import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
) 

class VideoIdRequest(BaseModel):
    video_id: str

def fetch_transcript(video_id):
    try:
        ytt_api = youtube_transcript_api.YouTubeTranscriptApi()
        return ytt_api.fetch(video_id, languages=['en', 'hi'])
    except TranscriptsDisabled:
        raise ValueError("Captions are disabled for this video")
    except NoTranscriptFound:
        raise ValueError("No transcript found for this video")
    except VideoUnavailable:
        raise ValueError("Video is unavailable or private")


app = FastAPI()

@app.post("/fetch_transcript")
async def get_trasncript(request: VideoIdRequest):
    transcript =  fetch_transcript(request.video_id) 
    return transcript

