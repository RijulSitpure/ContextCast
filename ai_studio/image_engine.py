import torch
from diffusers import StableDiffusionPipeline
import os

def generate_image(prompt, filename):
    model_path = "./sd_model"
    
    print(f"--- Loading Local Model ---")
    # We use local_files_only=True to ensure it never tries to download again
    pipe = StableDiffusionPipeline.from_pretrained(
        model_path, 
        local_files_only=True,
        use_safetensors=True
    )
    
    # Critical for MacBook Air speed: Use the Metal GPU
    if torch.backends.mps.is_available():
        pipe = pipe.to("mps")
        print("--- Using Mac GPU (MPS) ---")
    
    print(f"--- Generating: {prompt} ---")
    # num_inference_steps=20 is the 'sweet spot' for speed vs quality
    image = pipe(prompt, num_inference_steps=30).images[0]
    image.save(filename)
    print(f"--- Image saved as {filename} ---")

if __name__ == "__main__":
    generate_image("A futuristic neon podcast studio, cinematic lighting", "test_image.png")