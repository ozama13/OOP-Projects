class Car:
    def __init__(self,year, brand, model):
        self.year = year
        self.brand = brand
        self.model = model
        
mycar = Car()
mycar.year = 2013
mycar.brand = "Toyota"
mycar.model = "Camry"

print(mycar)
