from flask import Flask, render_template, Response, jsonify, request, send_from_directory
import cv2
import time
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from face_utils import recognize_person, get_fingerprint
from database import get_all_persons, update_embedding

# FLASK APP
app = Flask(__name__)

# Update this path to your actual known faces folder
KNOWN_FACES_DIR = r"C:\Users\shaky\OneDrive\Desktop\person recognization\known_faces"
UPLOAD_FOLDER = "static/uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# NEW ROUTE: SERVE IMAGES FROM DATABASE PATH
@app.route('/get_db_image/<filename>')
def get_db_image(filename):
    """Serves local system files as web URLs."""
    return send_from_directory(KNOWN_FACES_DIR, filename)

# DATABASE SYNC
def sync_database():
    print("Checking database fingerprints...")
    persons = get_all_persons()
    for p in persons:
        if p[9] is None:
            print(f"Generating fingerprint for: {p[1]}")
            embedding = get_fingerprint(p[8])
            if embedding is not None:
                update_embedding(p[0], embedding)
    print("System Ready")

sync_database()

# LIVE PERSON DATA
live_person_data = {
    "status": "Scanning...",
    "name": "Unknown",
    "similarity": "0%",
    "image": "/static/images/unknown.png",
    "age": "-", "gender": "-", "phone": "-", "address": "-", "email": "-", "occupation": "-", "message": "Waiting..."
}

# CAMERA & FACE DETECTION
def generate_frames():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # for low ram devices
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Save temp frame for analysis
        temp_path = "static/temp_live.jpg"
        cv2.imwrite(temp_path, frame)
        
        # Recognize
        result = recognize_person(temp_path)
        
        # Update global live data
        live_person_data.update(result)
        
        # Format image path for browser if verified
        if result["status"] != "UNKNOWN PERSON" and result["image"]:
            img_filename = os.path.basename(result["image"])
            live_person_data["image"] = f"/get_db_image/{img_filename}"

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/person_data')
def get_person_data():
    return jsonify(live_person_data)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"status": "Error", "message": "No file"})
    
    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    result = recognize_person(filepath)
    
    # Format image path for browser
    if result["status"] != "UNKNOWN PERSON" and result["image"]:
        img_filename = os.path.basename(result["image"])
        result["image"] = f"/get_db_image/{img_filename}"
        
    return jsonify(result)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)