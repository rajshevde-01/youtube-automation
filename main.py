import sys
import os
from database import init_db, has_uploaded_today, log_upload
from topic_generator import get_daily_topic
from script_generator import generate_script
from tts_engine import generate_audio
from video_generator import create_video
from youtube_uploader import upload_video

def main():
    print("Starting Daily YouTube Shorts Automation...")
    
    init_db()
    
    if has_uploaded_today():
        print("Already uploaded a video today. Exiting.")
        sys.exit(0)
        
    topic = get_daily_topic()
    script_data = generate_script(topic)
    
    audio_path = "temp_audio.wav"
    video_path = "temp_video.mp4"
    
    try:
        generate_audio(script_data['full_text'], audio_path)
        create_video(audio_path, script_data, video_path)
        
        # Upload to YouTube
        desc = f"{script_data['full_text']}\n\n#shorts #cybersecurity #tech #news"
        
        url = upload_video(
            video_path=video_path,
            title=script_data['title'],
            description=desc
        )
        log_upload(topic['title'], script_data['title'], "SUCCESS", url)
        print(f"Successfully uploaded! URL: {url}")
        
    except Exception as e:
        print(f"Failed to complete workflow: {e}")
        log_upload(topic['title'], script_data['title'], "FAILED", "")
        sys.exit(1)
        
    finally:
        # Cleanup temp files
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)

if __name__ == "__main__":
    main()
