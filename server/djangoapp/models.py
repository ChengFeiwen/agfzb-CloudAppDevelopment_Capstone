from django.db import models
from django.utils.timezone import now

# Create your models here.

# Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=30, null=False, default='CarMake')
    description = models.CharField(max_length=30, null=False, default='Description')
    
    def __str__(self):
        return "CarMake name: " + self.name

# Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):

    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    carmake = models.ForeignKey(CarMake, null=True, on_delete=models.SET_NULL)
    dealerid = models.IntegerField(null=True)
    name = models.CharField(max_length=30, null=False, default='CarModel')
    cartype = models.CharField(max_length=30, null=False, choices=TYPE, default=SEDAN)
    year = models.DateField(null=True)

    def __str__(self):
        return "CarMake name: " + self.name

# Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# Create a plain Python class `DealerReview` to hold review data
class DealerReview: 
    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, purchase_date,review,sentiment):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment
    
    def __str__(self):
        return "Review id: " + self.id

