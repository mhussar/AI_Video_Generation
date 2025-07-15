# server.py - Quick fix version
import base64, os, json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from app import analyze_image_with_gemma

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# serve the frontend - serve your existing mood.html
@app.route("/", methods=["GET"])
def root():
    return send_file("vanillajs/mood.html")


def root():
    return send_file("mood.html")




@app.route("/extract", methods=["POST"])
def extract_images():
    try:
        images = request.get_json(force=True)
        saved = []
        prompts = {}

        for img in images:
            filename = img["filename"]
            data = base64.b64decode(img["data"])
            path = os.path.join(UPLOAD_FOLDER, filename)
            with open(path, "wb") as f:
                f.write(data)
            saved.append(filename)
            
            # Add error handling for image analysis
            try:
                prompts[filename] = analyze_image_with_gemma(path)
            except Exception as e:
                print(f"Error analyzing image {filename}: {e}")
                prompts[filename] = f"Error analyzing image: {str(e)}"

        # Save to a more descriptive filename
        with open("image_prompts.json", "w", encoding="utf-8") as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)

        return jsonify({"saved_images": saved, "prompts": prompts, "status": "success"})
    
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5003)

