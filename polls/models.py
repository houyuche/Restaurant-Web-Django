from django.db import models

# Create your models here.

# class Menu(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.CharField(max_length=255, blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     count = models.IntegerField()
#     category = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.name



    
class LoginCredentials(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    reward_points = models.FloatField(default=0.0)
    shopping_cart = models.JSONField(default=list)
    
    def __str__(self):
        return self.username
    
class AvailableTimeSlots(models.Model):
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    MEAL_CHOICES = [
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]
    date = models.DateField()
    meal = models.CharField(max_length=20, choices=MEAL_CHOICES)
    capacity = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.date} - {self.get_meal_display()}"


class Reservations(models.Model):
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed'),
    ]

    username = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE)
    head_count = models.IntegerField(default=1)
    time_slot = models.ForeignKey(AvailableTimeSlots, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=CONFIRMED)

    def __str__(self):
        return f"Reservation for {self.username.username} on {self.time_slot.date} - {self.time_slot.get_meal_display()}"


class OrderHistory(models.Model):
    IN_PROGRESS = 'in progress'
    CANCELED = 'canceled'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed'),
    ]

    username = models.ForeignKey(LoginCredentials, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    items_ordered = models.JSONField(default=list)
    reward_change = models.FloatField(default=0.0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=IN_PROGRESS)

    def __str__(self):
        return f"Order by {self.username.username} at {self.time}"

