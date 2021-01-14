from flask import Blueprint, request, url_for
from flask_jwt_extended import jwt_required
from api.utils import File
from api.utils.responses import response_with
import api.utils.responses as resp
from api.models.authors import Author, AuthorSchema
from api.utils.database import db

author_routes = Blueprint("author_routes", __name__)


@author_routes.route('/avatar/<int:author_id>', methods=['POST'])
@jwt_required
def upsert_author_avatar(author_id):
    try:
        file = request.files['avatar']
        filename = ''
        get_author = Author.query.get_or_404(author_id)
        file_schema = File()
        if file and file_schema.allowed_file(filename=file.content_type):
            filename = file_schema.get_filename(file=file)
        get_author.avatar = url_for(
            'uploaded_file',
            filename=filename,
            _external=True
        )
        db.session.add(get_author)
        db.session.commit()
        author_schema = AuthorSchema()
        author = author_schema.dump(get_author)
        return response_with(resp.SUCCESS_201, value={'author': author})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/', methods=['POST'])
@jwt_required
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data)
        result = author_schema.dump(author.create())
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as e:
        print(e)
    return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/', methods=['GET'])
@jwt_required
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=['books', 'avatar', 'first_name', 'last_name', 'id'])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'authors': authors})


@author_routes.route('/<int:author_id>', methods=['GET'])
@jwt_required
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'author': author})


@author_routes.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get_or_404(id)
    if data.get('first_name'):
        get_author.first_name = data.get('first_name')
    if data.get('last_name'):
        get_author.last_name = data.get('last_name')
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={'author': author})


@author_routes.route('/<int:id>', methods=['PATCH'])
@jwt_required
def modify_author_detail(id):
    data = request.get_json()
    get_author = Author.query.get(id)
    if data.get('first_name'):
        get_author.first_name = data['first_name']
    if data.get('last_name'):
        get_author.last_name = data['last_name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return response_with(resp.SUCCESS_200, value={'author': author})


@author_routes.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_author(id):
    get_author = Author.query.get_or_404(id)
    db.session.delete(get_author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)
