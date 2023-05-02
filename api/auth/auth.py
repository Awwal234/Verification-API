from flask_restx import Namespace, Resource, fields
from ..models.user import User
from http import HTTPStatus
from flask import request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('auth', description='user authentication schema')
signup_model = auth_namespace.model('SignUp', {
    'id': fields.Integer(),
    'full_name': fields.String(required=True, description='User full name'),
    'email': fields.String(required=True, description='User unique email'),
    'password': fields.String(required=True, description='User unique password')
})
login_model = auth_namespace.model('Login', {
    'email': fields.String(required=True, description='User unique email'),
    'password': fields.String(required=True, description='User unique password')
})


@auth_namespace.route('/signup')
class UserSignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        '''
            Signup schema for App Api
        '''
        data = request.get_json()
        full_name = data['full_name']
        email = data['email']
        password = generate_password_hash(data['password'])

        signup_user = User(full_name=full_name, email=email, password=password)
        signup_user.save()

        return signup_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class UserLogin(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        '''
            Login Schema for App Api
        '''
        data = request.get_json()
        email = data['email']
        password = data['password']

        check_user = User.query.filter_by(email=email).first()

        if (check_user is not None) and check_password_hash(check_user.password, password):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)

            response = {
                'access': access_token,
                'refresh': refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        '''
            Refresh Tokens
        '''

        email = get_jwt_identity()
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        response = {
            'access': access_token,
            'refresh': refresh_token
        }

        return response, HTTPStatus.OK


@auth_namespace.route('/getme')
class GetUserName(Resource):
    @jwt_required()
    def get(self):
        '''
            Get User Profile
        '''

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        get_name = user.full_name

        response = {
            'email': email,
            'name': get_name,
        }

        return response, HTTPStatus.OK
