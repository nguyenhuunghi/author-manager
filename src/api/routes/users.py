from flask import Blueprint, request, url_for, render_template_string
from flask_jwt_extended import create_access_token, jwt_required
from api.utils import File
from api.utils.responses import response_with
from api.utils.token import generate_verification_token, confirm_verification_token
import api.utils.responses as resp
from api.models.users import User, UserSchema
from api.utils.database import db
from api.utils.email import send_email

user_routers = Blueprint("user_routers", __name__)


@user_routers.route('/avatar/<int:user_id>', methods=['POST'])
@jwt_required
def upsert_user_avatar(user_id):
    try:
        file = request.files['avatar']
        filename = ''
        get_user = User.query.get_or_404(user_id)
        file_schema = File()
        if file and file_schema.allowed_file(file.content_type):
            filename = file_schema.get_filename(file=file)
        get_user.avatar = url_for(
            'uploaded_file',
            filename=filename,
            _external=True
        )
        db.session.add(get_user)
        db.session.commit()
        user_schema = UserSchema()
        user = user_schema.dump(get_user)
        return response_with(resp.SUCCESS_201, value={'user': user})
    except Exception as e:
        print(e)
    return response_with(resp.INVALID_INPUT_422)


@user_routers.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if User.find_by_username(data.get('username')) is not None or User.find_by_email(data.get('email')) is not None:
            return response_with(resp.INVALID_INPUT_422)
        data['password'] = User.generate_hash(data.get('password'))
        user_schema = UserSchema()
        user = user_schema.load(data)
        token = generate_verification_token(data.get('email'))
        verification_email = url_for(
            'user_routers.verify_email',
            token=token,
            _external=True
        )
        html = render_template_string(
            "<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p> <p><a href='{{ verification_email }}'>{{ verification_email }}</a></p> <br> <p>Thanks!</p>",
            verification_email=verification_email
        )
        subject = 'Please verify your email'
        send_email(user.email, subject, html)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201, value={"user": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routers.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_401)
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_verified:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={'message': 'E-mail verified, you can proceed to log in now.'})


@user_routers.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        if data.get('email'):
            current_user = User.find_by_email(data.get('email'))
        elif data.get('username'):
            current_user = User.find_by_username(data.get('username'))
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if current_user and not current_user.is_verified:
            return response_with(resp.BAD_REQUEST_400)
        if User.verify_hash(data.get('password'), current_user.password):
            access_token = create_access_token(identity=data.get('username'))
            user_schema = UserSchema()
            user = user_schema.dump(current_user)
            return response_with(resp.SUCCESS_200, value={'message': 'Logged in as {}'.format(current_user.username),
                                                          'access_token': access_token,
                                                          'user': user})
        else:
            return response_with(resp.UNAUTHORIZED_401, value={'message': 'Password is wrong'})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routers.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_user_detail(id):
    data = request.get_json()
    get_user = User.query.get_or_404(id)
    if data.get('username'):
        get_user.username = data.get('username')
    if data.get('email'):
        get_user.email = data.get('email')
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return response_with(resp.SUCCESS_200, value={'user': user})
