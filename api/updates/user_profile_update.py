from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..utils import db
from http import HTTPStatus

user_update_namespace = Namespace(
    'user_profile_update', description='Update user profile e.g Fullname, email and password')
full_model = user_update_namespace.model('FullModel', {
    'id': fields.Integer(),
    'full_name': fields.String(required=True, description='User full name'),
    'email': fields.String(required=True, description='User unique email'),
    'password': fields.String(required=True, description='User unique password')
})
update_model = user_update_namespace.model('Update', {
    'email': fields.String(required=True, description='User unique email'),
    'password': fields.String(required=True, description='User unique password')
})


@user_update_namespace.route('/update_user')
class updateUserProfile(Resource):
    @user_update_namespace.expect(update_model)
    @user_update_namespace.marshal_with(full_model)
    @jwt_required()
    def put(self):
        '''
            Update user profile
        '''

        data = user_update_namespace.payload
        current_profile_identity = get_jwt_identity()

        user_check = User.query.filter_by(
            email=current_profile_identity).first()
        full_name = data['full_name']
        email = data['email']
        password = data['password']

        if user_check:
            user_check.full_name = full_name
            user_check.email = email
            user_check.password = password

            db.session.commit()

            response = {
                "message": "Updated successfully",
                "update": user_check
            }

            return response, HTTPStatus.OK
        else:
            #looking out for better response here
            response = {
                "message": "Error, try again."
            }
            
            return response, HTTPStatus.UNAUTHORIZED