from flask import Flask
from flask_restful import Api
from api_with_flask.resources.hotel import Hotel, HotelList, CreateHotel

app = Flask(__name__)
api = Api(app)    

api.add_resource(HotelList, '/hotels')
api.add_resource(Hotel, '/hotels/<string:id>')
api.add_resource(CreateHotel``, '/hotel')

if __name__ == '__main__':
    app.run(debug=True)