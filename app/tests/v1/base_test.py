import sys
sys.path.append('../')
import json
import unittest

#local imports
from app import create_app
from app.api.v1.models.incidence_model import Incidence
from app.api.v1.models.user_model import Users

incidence_obj = Incidence()
user_obj = Users()

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.test_user = {
            "firstname": "larry",
            "lastname": "kubende",
            "othername": "karani",
            "password": "6398litein",
            "email": "karanilarry@gmail.com",
            "phoneNumber": "0701043047",
            "username": "larrythegeek"
            }
        self.redflag_data = {
             "createdBy": "Larry karani",
             "incidence_type" : "red-flag",
             "location": "123456,23434",
             "comment":"String"
         }      
        self.redflag_data_with_empty_created={
             "createdBy": " ",
             "incidence_type" : "red-flag",
             "location": "123456,23434",
             "comment":"String"
        }
        self.redflag_data_with_empty_type ={
             "createdBy": "Larry karani",
             "incidence_type" : " ",
             "location": "123456,23434",
             "comment":"String"
        }

        self.redflag_data_empty_location = {
             "createdBy": "Larry karani",
             "incidence_type" : "red-flag",
             "location": " ",
             "comment":"String"
         }
        self.redflag_data_empty_comment = {
             "createdBy": "Larry karani",
             "incidence_type" : "red-flag",
             "location": "123,3445",
             "comment":" "
         }
        self.redflag_data_invalid_location = {
             "createdBy": "Larry karani",
             "incidence_type" : "red-flag",
             "location": "long, lat",
             "comment":"String"
         }
        self.location_data = {
             "location": "3333,5555"
         }
        self.comment_data= {
             "comment": "hey you"
         }

        self.update_redflag_status = {
             "status": "3333,5555"
         }
         #user data
        self.user_data = {
            "firstname": "larry",
            "lastname": "kubende",
            "othername": "karani",
            "password": "6398litein",
            "email": "karanilarry@gmail.com",
            "phoneNumber": "0701043047",
            "username": "larrythegeek"
            }
        self.user_data_empty_firstname ={
            "firstname": " ",
            "lastname": "kubende",
            "othername": "karani",
            "password": "6398litein",
            "email": "karanilarry@gmail.com",
            "phoneNumber": "0701043047",
            "username": "larrythegeek"
        }
        self.user_data_empty_lastname = {
            "firstname": "larry",
            "lastname": " ",
            "othername": "karani",
            "password": "6398litein",
            "email": "karanilarry@gmail.com",
            "phoneNumber": "0701043047",
            "username": "larrythegeek"
        }
        self.user_data_empty_password = {
            "firstname": "larry",
            "lastname": "kubende ",
            "othername": "karani",
            "password": " ",
            "email": "karanilarry@gmail.com",
            "phoneNumber": "0701043047",
            "username": "larrythegeek"
        }
        self.user_data_invalid_email= {
            "firstname": "larry",
            "lastname": "kubesh",
            "othername": "karani",
            "password": "6398litein",
            "email": "karanilgmailcom",
            "phoneNumber": "0701043047",
            "username": "larrythegeek"
        }
        self.user_data_invalid_phone ={
            "firstname": "larry",
            "lastname": "kubesh",
            "othername": "karani",
            "password": "6398litein",
            "email": "karanilgmailcom",
            "phoneNumber": "070",
            "username": "larrythegeek"

        }
        self.user_data_empty_username = {
            "firstname": "larry",
            "lastname": "kubesh",
            "othername": "karani",
            "password": "6398litein",
            "email": "karanilgmailcom",
            "phoneNumber": "0701043047",
            "username": " "
        }

    def tearDown(self):
        """clean Db"""
        incidence_obj.counter = 1
        incidence_obj.db.clear()
        user_obj.db.clear()
        self.client=None

if __name__ == '__main__':
    unittest.main(verbosity=2)
