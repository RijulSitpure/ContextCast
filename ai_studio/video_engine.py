from moviepy import ImageClip, AudioFileClip

def create_video_segment(image_path, audio_path, output_path):
    print(f"--- Processing Video: {output_path} ---")
    
    try:
        # 1. Load audio
        audio = AudioFileClip(audio_path)
        
        # 2. Load image and set duration (Modern Syntax)
        # In MoviePy 2.0+, we use .with_duration() or just duration = x
        clip = ImageClip(image_path).with_duration(audio.duration)
        
        # 3. Attach audio (Modern Syntax)
        clip = clip.with_audio(audio)
        
        # 4. Write the file
        # We specify fps and codec for Mac compatibility
        clip.write_videofile(output_path, fps=24, codec="libx264")
        
        print(f"--- SUCCESS: Video rendered as {output_path} ---")
        
    except Exception as e:
        # If 'with_duration' fails, try the older 'set_duration' just in case
        try:
            clip = ImageClip(image_path).set_duration(audio.duration).set_audio(audio)
            clip.write_videofile(output_path, fps=24, codec="libx264")
        except:
            print(f"--- VIDEO ERROR: {e} ---")

if __name__ == "__main__":
    pass