import webargs
from flask_restplus import Resource, fields, Namespace
from flask_jwt_extended import get_jwt_identity, jwt_required
#local import 
from app.api.v2.models.incident import Incidents
from app.api.v2.validators.validate_incident import IncidenceSchema, UpdateLocationSchema

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}
v2_incident= Namespace('interventions', authorizations=authorizations, security='apikey')

incident_data = v2_incident.model('Interventions',{
                       'incidence_type' :fields.String(description='name of the user creating the red-flag'),       
                       'location' :fields.String(description='name of the user creating the red-flag'),
                       'comment': fields.String(description='name of the user creating the red-flag')
})
class Incidences(Resource, Incidents):
    @v2_incident.expect(incident_data)
    @v2_incident.doc(security='apikey')
    @jwt_required
    def post(self):
        '''Create a new incidence'''
        data = v2_incident.payload
        schema = IncidenceSchema()
        results=schema.load(data)

        #get errors if any
        errors = results.errors
        incidence_fields = ['createdBy', 'location', 'incidence_type', 'comment']
        for error in incidence_fields:
            if error in errors.keys():
                return{'message': errors[error][0]}, 400
        
        current_user = get_jwt_identity()
        new_instance = Incidents( 
                                  current_user,
                                  data['incidence_type'],
                                  data['location'],
                                  data['comment']
                                )
        new_instance.create_an_incident()
        id = len(new_instance.get_all_incidents())
        return {
                'status' : 201, 
                'data' : [{
                           'id' : id,   
                           'message' :  'Created incidence record'
                           }]
               }
    @v2_incident.doc(security='apikey')
    @jwt_required
    def get(self):

        '''gets all incidences available in the db'''
        incidents = self.get_all_incidents()
        if len(incidents) == 0:
            return {'status':200,
                     'message': 'No records available'}
        
        #convert the tuble to a list of dicts
        keys = ['id', 'createdon', 'createdby', 'type','location', 'status', 'comment']
        output = []
        for values in incidents:
            output.append(dict(zip(keys, values)))

        return {
                "status": 200,
                "data":output
                }

@v2_incident.header("Authorization", "Access tokken", required=True)
class AnIncident(Resource, Incidents):
    '''get a single incident'''
    @v2_incident.doc(security='apikey')
    @jwt_required
    def get(self, incident_id):
        '''Returns details of a specific incidence'''

        keys = ['id', 'createdon', 'createdby', 'type','location', 'status', 'comment']
        incident= self.get_an_incident(incident_id)
        if not incident:
            return {'message': 'Incident does not exist'}, 400

        output = dict(zip(keys, incident))
        return {
                 'status': 200,
                  'data': [output]
              }
    @v2_incident.doc(security='apikey')
    @jwt_required
    def delete(self, incident_id):
        '''deletes a specific incident'''
        incident= self.get_an_incident(incident_id)
        if not incident:
            return {'message': 'Incident with given id {} does not exist'.format(incident_id)}, 400
        self.delete_incident(incident_id)
        return {
             'status':200,
             'id' : incident[0],
             'message': 'record deleted successfully'
              }

update_location = {"location": webargs.fields.Str(required=True)}
#documentation
update_location_args_model = v2_incident.model(
        "update_location_args", {"location": fields.String(required=True)})

@v2_incident.header("Authorization", "Access tokken", required=True)
class UpdateLocation(Resource, Incidents):
    @v2_incident.doc(body=update_location_args_model, security='apikey')
    @jwt_required
    def patch(self, incident_id):
        '''changes location of an incidence'''

        data = v2_incident.payload
        if not data:
            return {'message':'Please input data'}, 400

        loc = data['location']
        
        if loc.strip() =='':
            return {'message': 'Please provide a valid location'}, 400
        schema = UpdateLocationSchema()
        results=schema.load(data)
        errors = results.errors
        update_location_field = ['location']
        for error in update_location_field:
            if error in errors.keys():
                return{'message': errors[error][0]}, 400
        
        target = self.get_an_incident(incident_id)
        if target[5] != 'Draft':
            return {"message": "You cant change location for this intervention its status is changed"}, 204

        if not target:
            return {'message': 'Incident does not exist'}, 404

        else:
            self.update_location(incident_id, data['location'])
            target = self.get_an_incident(incident_id)
            keys = ['id', 'createdon', 'createdby', 'type','location', 'status', 'comment']
            output = dict(zip(keys, target))
            return {
                 'status':200, 
                 "data" : [output],
                 "id" : target[0],
                 "message" : "Updated red-flag record’s location"
             }