'''This module incidence related inputs validation'''
import re
from marshmallow import Schema, fields,  validates, ValidationError

def validate_length(input):
    if input.strip()=='':
        raise ValidationError({'message':'fields cannot be blank'})

class IncidenceSchema(Schema):
    '''Validates incidence data'''
    createdBy =    fields.String(required=True, validate=validate_length)
    location  = fields.String(required=True, validate=validate_length)
    comment   = fields.String(required=True,  validate=validate_length)
    incidence_type =fields.String(required=True, validate=validate_length)

    @validates('comment')
    def validate_comment(self, comment):
        r = re.compile("^[a-zA-Z ]*$")
        if comment.strip() == '':
            raise ValidationError('fields cannot be blank')
        elif not r.match(comment):
            raise ValidationError("{} is not a valid ".format(comment))

    @validates('location')
    def validate_location(self, location):
        r = re.compile("^[0-9]+(,[0-9]+)*$")
        if location.strip() == '':
            raise ValidationError('fields cannot be blank')
        elif not r.match(location):
            raise ValidationError("{} is not a valid location".format(location))
