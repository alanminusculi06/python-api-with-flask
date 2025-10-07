from flask_restful import Resource, reqparse
from models.hotel import HotelModel
import uuid


hotels = []

class HotelResource(Resource):
    def parse_args(self):
        hotel_parser = reqparse.RequestParser()
        hotel_parser.add_argument("name", type=str)
        hotel_parser.add_argument("stars", type=str)
        hotel_parser.add_argument("price", type=float)
        hotel_parser.add_argument("city", type=str)
        return hotel_parser.parse_args()
    
    def get_by_id(self, id):
        return next((hotel for hotel in hotels if hotel["id"] == id), None)
    
    def post(self):
        data = self.parse_args()
        new_hotel = HotelModel(self.new_id(), **data).to_dict()
        hotels.append(new_hotel)
        return new_hotel, 201
    
    def delete(self, id):
        hotel = self.get_by_id(id)
        if hotel:
            hotels.remove(hotel)
            return {"message": "Hotel deleted"}, 200
    
        return {"message": "Hotel not found"}, 404
    
    def get(self, id):
        hotel = self.get_by_id(id)
        if hotel:
            return hotel
        return {"message": "Hotel not found"}, 404
    
    def put(self, id):
        data = self.parse_args()
        new_hotel = HotelModel(id, **data).to_dict()
        
        hotel = self.get_by_id(id)
        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200
        
        return self.post(), 201
    
    def new_id(self):
        return str(uuid.uuid4())
    

class HotelList(Resource):
    def get(self):
        return {"hotels": hotels}
    
class Hotel(HotelResource):
    def get(self, id):
        return super().get(id)
    
    def put(self, id):
        return super().put(id)
    
    def delete(self, id):
        return super().delete(id)
    
    
class CreateHotel(HotelResource):
    def post(self):
        return super().post()
    
