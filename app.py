from flask import Flask, render_template, request, send_from_directory
import os
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Read and apply Canny
    img = cv2.imread(filepath)
    edges = cv2.Canny(img, 100, 200)

    output_path = os.path.join(OUTPUT_FOLDER, 'edges.png')
    cv2.imwrite(output_path, edges)

    return render_template('index.html', filename='edges.png')

@app.route('/static/<filename>')
def send_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)