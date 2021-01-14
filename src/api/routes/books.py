from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from api.utils.responses import response_with
import api.utils.responses as resp
from api.models.books import Book, BookSchema
from api.utils.database import db

book_routers = Blueprint("book_routers", __name__)


@book_routers.route('/', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(data)
        result = book_schema.dump(book.create())
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as e:
        print(e)
    return response_with(resp.INVALID_INPUT_422)


@book_routers.route('/', methods=['GET'])
@jwt_required
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True, only=['author_id', 'title', 'year'])
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'books': books})


@book_routers.route('/<int:id>', methods=['GET'])
@jwt_required
def get_book_detail(id):
    fetched = Book.query.get_or_404(id)
    book_schema = BookSchema()
    book = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={'book': book})


@book_routers.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get_or_404(id)
    get_book.title = data.get('title')
    get_book.year = data.get('year')
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={'book': book})


@book_routers.route('/<int:id>', methods=['PATCH'])
@jwt_required
def modify_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get_or_404(id)
    if data.get('title'):
        get_book.title = data.get('title')
    if data.get('year'):
        get_book.year = data.get('year')
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={'book': book})


@book_routers.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_book(id):
    get_book = Book.query.get_or_404(id)
    db.session.delete(get_book)
    db.commit()
    return response_with(resp.SUCCESS_204)
