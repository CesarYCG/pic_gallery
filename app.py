from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

app = Flask(__name__)
app.config["SECRET_KEY"] = "admin"
app.config["UPLOADED_PHOTOS_DEST"] = "img_uploads"

photos = UploadSet('photos',IMAGES) # Collecton of files
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File filed should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"],filename)


@app.route("/", methods=["GET","POST"])
def upload_image():
    form = UploadForm() # Instance
    if form.validate_on_submit(): # Validating the form
        filename = photos.save(form.photo.data) # Saving photo file
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template('index.html', form = form, file_url=file_url)

if __name__ == '__main__':
    app.run(debug=True)