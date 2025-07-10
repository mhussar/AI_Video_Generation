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

# Example usage
if __name__ == "__main__":
    # Make sure you have the model pulled first
    # Run: ollama pull gemma3:4b
    
    image_dir = r"images"
    prompt = """
    From the input image, extract a detailed image generation prompt using natural language. Do not include formatting, lists, titles, or commentary. 
    Output only coherent text that describes the image, suitable for an image generation model.
    """
    
   #initialize empty dicttionary
   
    
prompts = {}   
  #for loops through every image in the images folder and gives a prompt for each picture  
for image in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image)
        result = analyze_image_with_gemma(image_path, prompt)
        print(result)
        prompts[image] = result
        
        #dump prompts into json 
with open("image_prompt.json", 'w', encoding='utf-8') as f:
    json.dump(prompts, f, indent=2, ensure_ascii=False)

  
 
