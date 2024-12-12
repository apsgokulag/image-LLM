import requests

def test_image_upload():
    # URL of the Flask server's upload endpoint
    url = 'http://127.0.0.1:5000/upload'
    
    # Path to the test image you want to upload
    image_path = 'D:/DEVELOP/yolov3-master/image-upload/test_images/test_image.jpg'
    
    # Open the image in binary mode and prepare it for uploading
    files = {'image': open(image_path, 'rb')}
    
    try:
        # Set timeout to a larger value (e.g., 180 seconds = 3 minutes)
        print(f"🖼️ Test Image Path: {image_path}")
        response = requests.post(url, files=files, timeout=180)  # Increase the timeout to 180 seconds (3 minutes)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Print the response JSON (which will include the image URL and descriptions)
        print("Upload Success:", response.json())
    
    except requests.exceptions.Timeout:
        print("❌ Upload Failed - Timeout Error")
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload Failed - Error: {e}")
    finally:
        # Always close the file after the request is completed
        files['image'].close()

# Run the test
if __name__ == "__main__":
    test_image_upload()
