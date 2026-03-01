import os

def generate_audio(text, output_file="output.wav"):
    # Since Coqui TTS v0.22.0 is heavy to import, we import it inside the function
    print(f"Loading Coqui TTS model... This may take a minute first time.")
    from TTS.api import TTS
    
    # ljspeech/vits is widely used and sounds natural
    model_name = "tts_models/en/ljspeech/vits"
    tts = TTS(model_name=model_name, progress_bar=False, gpu=False)
    
    print(f"Generating audio to {output_file}...")
    tts.tts_to_file(text=text, file_path=output_file)
    print("Audio generation complete.")
    return output_file
