import base64
from io import BytesIO
from flask import Flask, request, send_file, render_template
import os
import subprocess
import uuid

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ... other imports and code


@app.route("/randomize_image", methods=["POST"])
def randomize_image():
    input_image = request.files.get("input_image")
    if not input_image:
        return {"error": "No input image provided"}, 400

    file_id = uuid.uuid4().hex
    input_image_path = f"temp/{file_id}_input.jpg"
    shuffled_output_image_path = f"temp/{file_id}_shuffled.jpg"
    unshuffled_output_image_path = f"temp/{file_id}_unshuffled.jpg"

    os.makedirs("temp", exist_ok=True)
    input_image.save(input_image_path)

    subprocess.run([
        "python3", "image_randomizer.py",
        input_image_path,
        shuffled_output_image_path,
        unshuffled_output_image_path
    ])

    os.remove(input_image_path)

    with open(shuffled_output_image_path, "rb") as f:
        shuffled_base64 = base64.b64encode(f.read()).decode("utf-8")

    with open(unshuffled_output_image_path, "rb") as f:
        unshuffled_base64 = base64.b64encode(f.read()).decode("utf-8")

    return render_template(
        "output.html",
        shuffled_image=f"data:image/jpeg;base64,{shuffled_base64}",
        unshuffled_image=f"data:image/jpeg;base64,{unshuffled_base64}",
    )



@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    try:
        return send_file(f"temp/{filename}", as_attachment=True)
    except FileNotFoundError:
        return {"error": "File not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
