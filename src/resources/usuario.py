from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
import uuid


class UserResource(Resource):
    def parse_args(self):
        hotel_parser = reqparse.RequestParser()
        hotel_parser.add_argument("name", type=str, required=True, help="The field 'name' cannot be left blank")
        hotel_parser.add_argument("login", type=str, required=True, help="The field 'stars' cannot be left blank")
        hotel_parser.add_argument("password", type=str, required=True, help="The field 'price' cannot be left blank")
        return hotel_parser.parse_args()
    
    def get_by_id(self, id):
        return UsuarioModel.find_by_id(id)
    
    def post(self):
        data = self.parse_args()
        
        user = UsuarioModel.find_by_login(data['login'])
        if user:
            return {"message": "A user with that login already exists."}, 400
        
        try:
            new_hotel = UsuarioModel(self.new_id(), **data)
            new_hotel.save()
            return new_hotel.to_dict(), 201
        except:
            return {"message": "An internal error ocurred trying to save user."}, 500
    
    @jwt_required()
    def delete(self, id):
        user = self.get_by_id(id)
        if user:
            try:
                user.delete()
            except:
                return {"message": "An internal error ocurred trying to delete user."}, 500
            return {"message": "User deleted"}, 200
    
        return {"message": "User not found"}, 404
    
    def get(self, id):
        hotel = self.get_by_id(id)
        if hotel:
            return hotel.to_dict()
        return {"message": "User not found"}, 404
    
    def new_id(self):
        return str(uuid.uuid4())
    
    
class User(UserResource):
    def get(self, id):
        return super().get(id)
    
    def put(self, id):
        return super().put(id)
    
    def delete(self, id):
        return super().delete(id)
    
    
class CreateUser(UserResource):
    def post(self):
        return super().post()
    
class UserLogin(Resource):
    def parse_args(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument("login", type=str, required=True, help="The field 'login' cannot be left blank")
        user_parser.add_argument("password", type=str, required=True, help="The field 'password' cannot be left blank")
        return user_parser.parse_args()
    
    def post(self):
        data = self.parse_args()
        
        user = UsuarioModel.find_by_login(data['login'])
        if user and user.verify_password(data['password']):
            token = create_access_token(identity=user.id)
            return {"access_token": token}, 200
        return {"message": "Invalid credentials."}, 401