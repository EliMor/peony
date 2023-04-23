from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_type = filename.split(".")[-1].lower()

            if file_type == "pdf":
                # Do something with PDF file
                result = "PDF file selected."
            elif file_type in ["jpg", "jpeg", "png"]:
                # Resize and save image
                image = Image.open(file)
                image = image.resize((300, 300))
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result = "Image file selected."
            elif file_type in ["mp4", "mov", "avi"]:
                # Play video using subprocess
                subprocess.call(['vlc', os.path.join(app.config['UPLOAD_FOLDER'], filename)])
                result = "Video file selected."
            else:
                result = "Invalid file type selected."
            return render_template('index.html', result=result)
    return render_template('index.html', result='')

if __name__ == '__main__':
    app.run(debug=True)
