import os

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from GPSPhoto import gpsphoto
import folium
import subprocess
from loguru import logger

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["ALLOWED_EXTENSIONS"] = set(
    ["pdf", "jpg", "jpeg", "png", "mp4", "mov", "avi"]
)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            file_type = filename.split(".")[-1].lower()

            if file_type == "pdf":
                # Do something with PDF file
                result = "PDF file selected."
            elif file_type in ["jpg", "jpeg", "png"]:
                # Resize and save image
                data = gpsphoto.getGPSData(
                    os.path.join(app.config["UPLOAD_FOLDER"], filename)
                )
                logger.info(data)
                location = [data["Latitude"], data["Longitude"]]
                map = folium.Map(location=location)
                return_page = result = "dynamic.html"
                map.save(f"/app/static/{return_page}")

            elif file_type in ["mp4", "mov", "avi"]:
                # Play video using subprocess
                subprocess.call(
                    ["vlc", os.path.join(app.config["UPLOAD_FOLDER"], filename)]
                )
                result = "Video file selected."
            else:
                result = "Invalid file type selected."
            return render_template("index.html", result=result)
    return render_template("index.html", result="")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
