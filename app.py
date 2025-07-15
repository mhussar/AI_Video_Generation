import ollama
from PIL import Image
import base64
import io
import os
import json

# Function to encode image as base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Basic usage with Ollama
def analyze_image_with_gemma(image_path, prompt="Describe this image but do so as a coherent image prompt. Do not give me a list."):
    try:
        # Encode the image
        base64_image = encode_image(image_path)
        
        # Create the message with image
        response = ollama.chat(
            model='gemma3:4b',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [base64_image]
            }]
        )
        
        return response['message']['content']
    except Exception as e:
        print(f"Error in analyze_image_with_gemma: {e}")
        return f"Error analyzing image: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Make sure you have the model pulled first
    # Run: ollama pull gemma3:4b
    
    image_dir = "images"
    prompt = """
    From the input image, extract a detailed image generation prompt using natural language. Do not include formatting, lists, titles, or commentary. 
    Output only coherent text that describes the image, suitable for an image generation model.
    """
    
    # Initialize empty dictionary
    prompts = {}
    
    # Check if images directory exists
    if not os.path.exists(image_dir):
        print(f"Directory {image_dir} does not exist!")
        exit(1)
    
    # Get list of image files
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if not image_files:
        print("No image files found in the images directory!")
        exit(1)
    
    # Process each image
    for image in image_files:
        image_path = os.path.join(image_dir, image)
        try:
            result = analyze_image_with_gemma(image_path, prompt)
            print(f"Processed {image}: {result[:100]}...")  # Show first 100 chars
            prompts[image] = result
        except Exception as e:
            print(f"Error processing {image}: {e}")
            prompts[image] = f"Error: {str(e)}"
    
    # Save prompts to JSON
    with open("image_prompts.json", 'w', encoding='utf-8') as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(prompts)} images. Results saved to image_prompts.json")