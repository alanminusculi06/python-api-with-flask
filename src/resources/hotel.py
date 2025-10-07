from flask_restful import Resource, reqparse
from models.hotel import HotelModel
import uuid


hotels = []

class HotelResource(Resource):
    def parse_args(self):
        hotel_parser = reqparse.RequestParser()
        hotel_parser.add_argument("name", type=str, required=True, help="The field 'name' cannot be left blank")
        hotel_parser.add_argument("stars", type=str, required=True, help="The field 'stars' cannot be left blank")
        hotel_parser.add_argument("price", type=float, required=True, help="The field 'price' cannot be left blank")
        hotel_parser.add_argument("city", type=str, required=True, help="The field 'city' cannot be left blank")
        return hotel_parser.parse_args()
    
    def get_by_id(self, id):
        return HotelModel.find_hotel_by_id(id)
    
    def post(self):
        data = self.parse_args()
        new_hotel = HotelModel(self.new_id(), **data)
        try:
            new_hotel.save()
        except:
            return {"message": "An internal error ocurred trying to save hotel."}, 500
        return new_hotel.to_dict(), 201
    
    def delete(self, id):
        hotel = self.get_by_id(id)
        if hotel:
            try:
                hotel.delete()
            except:
                return {"message": "An internal error ocurred trying to delete hotel."}, 500
            return {"message": "Hotel deleted"}, 200
    
        return {"message": "Hotel not found"}, 404
    
    def get(self, id):
        hotel = self.get_by_id(id)
        if hotel:
            return hotel.to_dict()
        return {"message": "Hotel not found"}, 404
    
    def put(self, id):
        data = self.parse_args()
        
        hotel = self.get_by_id(id)
        if hotel:
            try:
                hotel.update(**data)
            except:
                return {"message": "An internal error ocurred trying to update hotel."}, 500
            return hotel.to_dict(), 200
        
        return {"message": "Hotel not found"}, 404
    
    def new_id(self):
        return str(uuid.uuid4())
    

class HotelList(Resource):
    def get(self):
        return {"hotels": [] if not HotelModel.query.all() else [hotel.to_dict() for hotel in HotelModel.query.all()]}
    
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
    
