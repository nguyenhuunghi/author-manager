import os
from flask import current_app
from werkzeug.utils import secure_filename


class File(object):
    allowed_extensions = set(['image/jpeg', 'image/png', 'image/jpeg'])

    def allowed_file(self, filename):
        return filename in self.allowed_extensions

    def get_filename(self, file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename
