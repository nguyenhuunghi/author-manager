import os, sys, logging
import flask_monitoringdashboard as dashboard
from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask import jsonify
from api.config.config import Production, Development, Testing
from api.utils.database import db
from api.utils.responses import response_with
from api.utils.email import mail
import api.utils.responses as resp
from api.routes.authors import author_routes
from api.routes.books import book_routers
from api.routes.users import user_routers


if os.environ.get('WORK_ENV') == 'PROD':
    app_config = Production
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = Testing
else:
    app_config = Development


def create_app(config):
    # that is skeleton of main
    app = Flask(__name__)

    app.register_blueprint(author_routes, url_prefix='/api/authors')
    app.register_blueprint(book_routers, url_prefix='/api/books')
    app.register_blueprint(user_routers, url_prefix='/api/users')
    app.config.from_object(config)

    # START GLOBAL HTTP CONFIGURATION
    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)

    @app.route('/avatar/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    db.init_app(app)
    jwt = JWTManager(app)
    mail.init_app(app)
    dashboard.bind(app)
    with app.app_context():
        db.create_all()

    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
                        level=logging.DEBUG)

    return app


app = create_app(app_config)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', use_reloader=False)
