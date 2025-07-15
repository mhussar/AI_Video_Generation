from flask import Flask, request, jsonify
import base64
import os
from app import analyze_image_with_gemma
import json
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = "images"

os.makedirs(UPLOAD_FOLDER, exist_ok = True)

@app.route('/extract', methods = ['POST'])
def extract_images():
    images = request.json
    saved = []
    
    for img in images:
        filename = img['filename']
        data = base64.b64decode(img['data'])
        path = os.path.join(UPLOAD_FOLDER,filename)
        with open(path, 'wb') as f:
            f.write(data)
        saved.append(filename)
      
    prompt = {}  
    
    for filename in saved:
        image_path = os.path.join("images",filename)
        result = analyze_image_with_gemma(image_path)
        prompt[filename] =result
        
    with open("hi.json", 'w', encoding ='utf-8') as f:
        json.dump(prompt,f,indent=2,ensure_ascii = False)
        
        
        
    return jsonify({'saved images': saved, "status": "done"})


if __name__ == "__main__":
    app.run(debug=True)
