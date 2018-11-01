from flask_restful import Resource, abort


class HelloWorld(Resource):

    def __init__(self,**kwargs):
        self.config = kwargs['config']

    def get(self,fullName):
        return "Hello " + str(fullName) + "! How are you?"

