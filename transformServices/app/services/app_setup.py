from flask import Flask
from flask_restful import Api, Resource, abort

app = Flask('__main__')
api = Api(app)

from gleanomatic.configure import appConfig as config
from . import HelloWorld as hw

api.add_resource(hw,
                 "/HelloWorld/<string:fullName>",
                 methods=['GET'],
                 resource_class_kwargs={ 'config': config })

