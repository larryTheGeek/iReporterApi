import webargs
from flask_restplus import Resource, fields, Namespace
from flask_jwt_extended import create_access_token

#local import
from app.api.v2.models.users import User
from app.api.v2.validators.validate_user import UserSchema, LoginSchema

v2_user = Namespace('auth')

registration_args_model=v2_user.model(
    'Regestration', {
    "firstname": fields.String(description='username'),
    "lastname": fields.String(description='username'),
    "othername": fields.String(description='username'),
    "password": fields.String(description='password'),
    "email": fields.String(description='email'),
    "phoneNumber": fields.String(description='phoneNumber'),
    "username": fields.String(description='username')})

user_login = v2_user.model('Login', {'username': fields.String('email@example.com'),
                                     'password': fields.String('test_pass')})

class Register(Resource):
    @v2_user.expect(registration_args_model)
    def post(self):
        '''register a new user'''
        data = v2_user.payload
        schema = UserSchema()
        schema_data = schema.load(data)

        errors = schema_data.errors
        error_types = ['firstname', 'lastname', 'othername', 'password', 'email','phoneNumber','username']

        for e in error_types:
            if e in errors.keys():
                return {'message': errors[e][0]}, 400
        
        new_user = User(
                      data['firstname'],
                      data['lastname'],
                      data['othername'],
                      data['email'],
                      data['phoneNumber'],
                      data['username'],
                      data['password']
                     )
       #check if user already exists
        user = new_user.check_username(data['username'])
        if user:
            return {'message': 'username already exists'}, 400

        mail = new_user.check_email(data['email'])
        if mail:
            return {'message': 'email already exists'}, 400

        new_user.register_user()
        return {'message': 'user successfuly  added',
                 'data': data
                }, 201