from django.contrib import admin

# Register your models here.


from .models import LoginCredentials, OrderHistory, AvailableTimeSlots, Reservations

# admin.site.register(Menu)
admin.site.register(LoginCredentials)
admin.site.register(OrderHistory)
admin.site.register(AvailableTimeSlots)
admin.site.register(Reservations)