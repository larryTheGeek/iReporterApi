'''This module handles the validation of all data relating to the user'''

import re
from marshmallow import Schema, fields,  validates, ValidationError

def validate_length(input):
    if input.strip()=='':
        raise ValidationError({'message':'Fields cannot be blank'})
        
class UserSchema(Schema):
    '''schema for validating signup data'''
    firstname = fields.String(required=True, validate=validate_length)
    lastname = fields.String(required=True, validate=validate_length)
    othername = fields.String(required=True, validate=validate_length)
    email = fields.Email(required=True)
    phoneNumber = fields.String(required=True, validate=validate_length)
    username = fields.String(required=True, validate=validate_length)

    @validates('phoneNumber')
    def validate_phonenumber(self, phoneNumber):
        if len(phoneNumber)<10:
            raise ValidationError('Phone number should be 10 characters  long')

class LoginSchema(Schema):
    '''schema for validating login data'''
    username = fields.String(required=True, validate=validate_length)
    password = fields.String(required=True, validate=validate_length)
    