from flask import Flask, g, jsonify
from flask_restful import Api
from resources.hotel import Hotel, HotelList, CreateHotel
from resources.usuario import User, CreateUser, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
import BLOCKLIST

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Adicione esta linha
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)    

jwt = JWTManager(app)

@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()
        
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST.BLOCKLIST

# Callback function for when a revoked token is encountered
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (jsonify({"message": "The token has been revoked."}), 401)

api.add_resource(HotelList, '/hotels')
api.add_resource(Hotel, '/hotels/<string:id>')
api.add_resource(CreateHotel, '/hotel')
api.add_resource(User, '/users/<string:id>')
api.add_resource(CreateUser, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)