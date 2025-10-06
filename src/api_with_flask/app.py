from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Hotel(Resource):
    def get(self):
        return {"message": "Welcome to the Hotel API"}
    

api.add_resource(Hotel, '/hotels')

if __name__ == '__main__':
    app.run(debug=True)