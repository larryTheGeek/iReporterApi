[![Coverage Status](https://coveralls.io/repos/github/larryTheGeek/iReporterApi/badge.svg?branch=develop)](https://coveralls.io/github/larryTheGeek/iReporterApi?branch=develop)
[![Build Status](https://travis-ci.com/larryTheGeek/iReporterApi.svg?branch=develop)](https://travis-ci.com/larryTheGeek/iReporterApi)
[![Maintainability](https://api.codeclimate.com/v1/badges/55f6147ce61b0772db62/maintainability)](https://codeclimate.com/github/larryTheGeek/iReporterApi/maintainability)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# iReporterApi
iReporter is an application whose aim is to reduce corruption in Africa and foster economic development. It allows users to create red flags and interventions. It implents the following list of APIs.

### Framework used
The application is built using python: flask framework.
>[Flask](http://flask.pocoo.org/) is a microframework for the Python programming language.


### End points
Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `/api/v2/auth/signup` |  Register a user. |
|POST| `api/v2/auth/login` | Login user.|
|POST| `api/v2/auth/logout` | Logs out a user.|
|POST| `api/v2/interventions` | Create a new incident. |
|GET| `api/v2/interventions` | Get all the created incidents. |
|GET| `api/v2/interventions/user` | Get all incident of the logged in user. |
|GET| `api/v2/interventions/<incident_id>` | Get a single incident. |
|PATCH| `api/v2/interventions/<incident_id>/location` | Update a single incident location. |
|PATCH| `api/v2/interventions/<incident_id>/comment` | Update a single incident comment. |
|PATCH| `api/v2/interventions/<incident_id>/status` | Update a single incident status. |
|DELETE| `api/v2/interventions/<incident_id>` | Delete a single incident. |

## Installation 🕵
- To run on local machine git clone this project :
```
$ git clone https://github.com/larryTheGeek/iReporterApi.git
```
Copy and paste the above command in your terminal, the project will be downloaded to your local machine.

To Install python checkout:
```
https://www.python.org/
```

- create a virtualenv and make it use python 3 using the following command.
```
$ virtualenv -p python3 env
```
- activate the virtual environment
```
 $ source env/bin/activate
```
- Install Requirements
```
$ pip install -r requirements.txt
```
### Testing
- Run Test using pytest with the following command
```
$ py.test --cov=app test` 
```
you will get the test coverage report on your terminal


The app can also be tested via Postman
- Run App 
```
$ python run.py
```
The app should be accessiable via : http://127.0.0.1:5000/

open postman and navigate to the API endpoints described above

### HEROKU URL
 https://ireporter-version2.herokuapp.com/api/v2/
 
### Owner
- Larry Karani

### Motivation
https://www.youtube.com/watch?v=wHRUDL7GKmI




