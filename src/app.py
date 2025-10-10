from flask import Flask, g
from flask_restful import Api
from resources.hotel import Hotel, HotelList, CreateHotel
from resources.usuario import User, CreateUser, UserLogin
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'  # Adicione esta linha
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)    

jwt = JWTManager(app)

@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

api.add_resource(HotelList, '/hotels')
api.add_resource(Hotel, '/hotels/<string:id>')
api.add_resource(CreateHotel, '/hotel')
api.add_resource(User, '/users/<string:id>')
api.add_resource(CreateUser, '/users')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)