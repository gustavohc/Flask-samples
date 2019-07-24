from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
    )
from blacklist import BLACKLIST
from models.user import User

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                           type=str,
                           required=True,
                           help="This field cannot be left blank!"
)
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
)

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'This user already exists!'}, 400

        user = User(**data)
        user.save_to_db()

        return {'message': 'The has been crested!'}, 201

class UserResources(Resource):
    @classmethod
    def get(cls, user_id):
        user = User.find_by_id(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def delete(cls, user_id):
        user = User.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted!'}, 200
        return {'message': 'User not found'}, 404


class UserLogin(Resource):
    @classmethod
    def post(self):
        # get data from parser
        data = _user_parser.parse_args()

        #find user in database
        user = User.find_by_username(data['username'])

        #check password
        if user and safe_str_cmp(user.password, data['password']):
            #create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'User not found!'}, 404


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200
