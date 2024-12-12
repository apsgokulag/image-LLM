import openai
import os
import base64
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'your-api-key'

# Define your upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Function to generate descriptions
def generate_descriptions(base64_image):
    try:
        # Make the request to OpenAI's API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-4" instead of "gpt-4-turbo"
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please provide three distinct descriptions of this image: 1) A formal, professional description 2) A humorous, playful description 3) A critically analytical description"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error generating descriptions: {str(e)}"

# Route for uploading and processing the image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file found in the request'}), 400
    
    file = request.files['image']
    
    if file and allowed_file(file.filename):
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Convert the image to base64
        base64_image = image_to_base64(file_path)

        # Get descriptions from OpenAI
        descriptions = generate_descriptions(base64_image)

        # Return the generated descriptions along with the image URL
        return jsonify({
            'descriptions': descriptions,
            'image_url': f"/uploads/{filename}"
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
