from utils import code2name


class Purchase:
    def __init__(self, name, weight, measurement, quantity, full_weight, full_price):
        self.name = name
        self.weight = weight
        self.measurement = measurement
        self.quantity = quantity
        self.full_weight = full_weight
        self.full_price = full_price
        
    def __str__(self):
        return f"Name: {self.name}, Weight: {self.weight} {code2name[self.measurement]}, " \
    f"Quantity: {self.quantity}, Full weight: {self.full_weight} {code2name[self.measurement]} Full price: {self.full_price}"