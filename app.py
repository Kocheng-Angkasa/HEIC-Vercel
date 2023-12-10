from flask import Flask, request, render_template_string
import pyheif
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_heic():
    if request.method == 'POST':
        heic_bytes = request.files['file'].read()
        image = heic_to_jpeg(heic_bytes)
        return image_to_response(image)
    return render_template_string('<form method="post" enctype="multipart/form-data"><input type="file" name="file"><input type="submit"></form>')

def heic_to_jpeg(heic_bytes):
    heif_file = pyheif.read(heic_bytes)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    return image

def image_to_response(image):
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    return img_io.getvalue()

if __name__ == '__main__':
    app.run(debug=True)
