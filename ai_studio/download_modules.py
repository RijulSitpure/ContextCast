import torch
from diffusers import StableDiffusionPipeline
import os

# Your Token
HF_TOKEN = "YOUR_HUGGING_FACE_TOKEN_HERE"

def download_slim():
    print("--- Attempting Clean Download for MacBook Air ---")
    # Using the most direct model path
    model_id = "runwayml/stable-diffusion-v1-5"
    
    try:
        # We use 'use_safetensors=True' which is the modern standard for 2026
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            revision="fp16",
            torch_dtype=torch.float16,
            use_auth_token=MY_TOKEN,
            use_safetensors=True 
        )
        
        # Save it locally so we never have to deal with the Hub again
        pipe.save_pretrained("./sd_model")
        print("\n--- SUCCESS! Model saved in './sd_model' ---")
        
    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"The Hub is acting up. Let's try the direct approach without the revision flag.")
        try:
            # Fallback: Download the standard version if fp16 branch is hidden
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                use_auth_token=MY_TOKEN
            )
            pipe.save_pretrained("./sd_model")
            print("\n--- SUCCESS (Standard Version)! ---")
        except Exception as e2:
            print(f"Final Error: {e2}")

if __name__ == "__main__":
    download_slim()