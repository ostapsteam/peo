from flask_restful import Resource


class Lab(Resource):

    def get(self, id):
        return '1', 200

    def post(self):
        return "2", 200
