import os
from moviepy.editor import ColorClip, TextClip, AudioFileClip, CompositeVideoClip

def create_video(audio_file, script_data, output_file="output_shorts.mp4"):
    print("Generating video...")
    
    audio = AudioFileClip(audio_file)
    duration = audio.duration
    
    # 1080x1920 for YouTube Shorts
    w, h = 1080, 1920
    
    # Background: dark solid color
    bg = ColorClip(size=(w, h), color=(15, 20, 30)).set_duration(duration)
    
    # Title text (Hacker green)
    title_text = script_data.get("title", "Daily Cyber Short")
    title_clip = TextClip(
        title_text, 
        fontsize=70, 
        color='#00FF00', 
        font='Courier', 
        method='caption', 
        size=(w-100, None)
    ).set_position(('center', 300)).set_duration(duration)
    
    # Hook Text (Dynamic - bright white for contrast)
    hook_text = script_data.get("hook", "")
    hook_clip = TextClip(
        hook_text, 
        fontsize=60, 
        color='white', 
        font='Courier', 
        method='caption', 
        size=(w-150, None)
    ).set_position('center').set_duration(min(5.0, duration)).crossfadeout(1.0)
    
    # CTA Text (Matrix style bright green)
    cta_text = script_data.get("cta", "Subscribe to The Exploit Feed!")
    cta_clip = TextClip(
        cta_text, 
        fontsize=60, 
        color='#00FF00', 
        font='Courier', 
        method='caption', 
        size=(w-150, None)
    ).set_position('center')
    
    cta_start = max(0, duration - 5.0)
    cta_clip = cta_clip.set_start(cta_start).set_duration(duration - cta_start).crossfadein(1.0)

    # Combine
    video = CompositeVideoClip([bg, title_clip, hook_clip, cta_clip])
    video = video.set_audio(audio)
    
    print(f"Writing video to {output_file}...")
    video.write_videofile(
        output_file, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac", 
        preset="ultrafast", 
        threads=4,
        logger=None
    )
    
    print("Video generation complete.")
    return output_file
