import sys

# override the azureml.contrib.services package with local one, meanwhile keep the other stuff under azureml.* untouched
# note this must be done prior to importing the package in app logic

import azureml.contrib.services.aml_request
import azureml_contrib_services.aml_request

# works for 'import azureml.contrib.services.aml_request'
sys.modules["azureml.contrib.services"].aml_request = sys.modules["azureml_contrib_services"].aml_request
# works for 'from azureml.contrib.services.aml_request import *'
sys.modules["azureml.contrib.services.aml_request"] = sys.modules["azureml_contrib_services.aml_request"]

import azureml.contrib.services.aml_response
import azureml_contrib_services.aml_response

# works for 'import azureml.contrib.services.aml_response'
sys.modules["azureml.contrib.services"].aml_response = sys.modules["azureml_contrib_services"].aml_response
# works for 'from azureml.contrib.services.aml_response import *'
sys.modules["azureml.contrib.services.aml_response"] = sys.modules["azureml_contrib_services.aml_response"]


from flask import Flask
from routes import main


def create():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app


if __name__ == "__main__":
    app = create()
    app.run(host="0.0.0.0", port=31311)
