from sql_alchemy import db


class HotelModel(db.Model):
    __tablename__ = 'hotels'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))
    stars = db.Column(db.String(1))
    price = db.Column(db.Float(precision=2))
    city = db.Column(db.String(40))
    
    def __init__(self, id, name, stars, price, city): 
        self.id = id
        self.name = name
        self.stars = stars
        self.price = price
        self.city = city

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "stars": self.stars,
            "price": self.price,
            "city": self.city
        }
        
    @classmethod
    def find_hotel_by_id(cls, id):
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self, name, stars, price, city):
        self.name = name
        self.stars = stars
        self.price = price
        self.city = city
        self.save() 
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()