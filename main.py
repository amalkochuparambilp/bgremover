import os
from flask import Flask, request, render_template
from rembg import remove
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        return render_template('result.html', output_image='output.png')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if not allowed_file(file.filename):
        return 'File type not allowed'

if __name__ == '__main__':
    app.run(debug=True)