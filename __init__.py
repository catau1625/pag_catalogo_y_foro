from flask import Flask
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/cataubilla/Desktop/Escritorio_cataubilla/coding_dojo/proyectos/foro_perfumes/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'SuperClaveSecreta'
bcrypt = Bcrypt(app)