from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('order_history/', views.order_history, name='order_history'),
    path('place_order/', views.place_order, name='place_order'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('available_time/', views.get_avalaible_time, name='available_time'),
    path('reservations/', views.get_reservation, name='reservations'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('cancel_reservation/', views.cancel_reservation, name='cancel_reservation'),
    path('reset_data/', views.reset_data, name='reset_data')
]