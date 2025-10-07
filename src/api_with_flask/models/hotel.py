class HotelModel:
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