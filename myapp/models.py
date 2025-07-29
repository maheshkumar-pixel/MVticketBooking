from django.db import models
from django.contrib.auth.models import User

class Ticketbook(models.Model):
    BUS_TYPE_CHOICES = [
        ('ordinary', 'Ordinary Bus'),
        ('ac', 'AC Bus'),
        ('sleeper', 'Sleeper Coach'),
    ]
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES)
    ticket_amount=models.CharField(max_length=20)
    seat_number = models.CharField(max_length=10)
    select_date = models.DateField()  # Changed from travel_date to match admin
    select_time = models.TimeField()  # Changed from travel_time to match admin
    
    def __str__(self):
        return f"{self.name} - {self.source} to {self.destination}"
    from django.db import models

class TripPackage(models.Model):
    cust_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    no_of_tickets=models.IntegerField()
    places = models.JSONField()  # ✅ Stores list of places
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
