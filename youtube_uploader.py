import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def get_authenticated_service():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        raise ValueError("Missing YouTube credentials in environment. Need YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN.")

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    return build("youtube", "v3", credentials=credentials)

def upload_video(video_path, title, description, tags=None):
    if tags is None:
        tags = ["shorts", "cybersecurity", "tech", "automation", "infosec"]
        
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title[:100],  # Title max 100 chars
            "description": description[:5000],  # Desc max 5000 chars
            "tags": tags,
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"Uploading {video_path} to YouTube...")
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )
    
    response = insert_request.execute()
    video_id = response.get("id")
    print(f"Upload successful! Video ID: {video_id}")
    return f"https://www.youtube.com/shorts/{video_id}"
