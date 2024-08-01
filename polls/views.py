from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import LoginCredentials, OrderHistory, AvailableTimeSlots, Reservations
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
import json
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

def user_login(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if not LoginCredentials.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username not found'})

    user = LoginCredentials.objects.get(username=username)

    if check_password(password, user.password):
        return JsonResponse({'status': 'success', 'reward': user.reward_points, 'cart':user.shopping_cart})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})
    

def user_signup(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if LoginCredentials.objects.filter(username=username).exists():
        return JsonResponse({'status': 'error', 'message': 'Username already exists'})

    user = LoginCredentials.objects.create(
        username=username,
        password=make_password(password),
    )
    user.save()
    return JsonResponse({'status': 'success', 'message': 'User created successfully'})


# def rewards(request):
#     username = request.GET.get('username')
#     user = LoginCredentials.objects.get(username=username)
#     return JsonResponse({'reward': user.reward_points})

# def change_password(request):
#     username = request.GET.get('username')
#     user = LoginCredentials.objects.get(username=username)
#     newpassword = request.GET.get('password')
#     user.password = make_password(newpassword)
#     user.save(update_fields=['password'])
#     return JsonResponse({'status': 'success', 'message': 'Password change successfully'})


def order_history(request):
    username = request.GET.get('username')
    orders = OrderHistory.objects.filter(username__username=username).values()
    return JsonResponse(list(orders), safe=False)


def get_avalaible_time(request):
    check_date = request.GET.get('date')
    time = AvailableTimeSlots.objects.filter(date=check_date)
    return JsonResponse(list(time), safe=False)

def get_reservation(request):
    username = request.GET.get('username')
    reservations = Reservations.objects.filter(username__username=username).values()
    return JsonResponse(list(reservations), safe=False)


@csrf_exempt
def make_reservation(request):
    data = json.loads(request.body)
    username = data.get('username')
    time_slot_id = data.get('time_slot_id')
    head_count = data.get('head_count')

    user = LoginCredentials.objects.get(username=username)
    time_slot = AvailableTimeSlots.objects.get(id=time_slot_id)

    reservation = Reservations.objects.create(
            username=user,
            head_count=int(head_count),
            time_slot=time_slot,
            status=Reservations.CONFIRMED
        )
    reservation.save()
    
    time_slot.capacity -= int(head_count)
    time_slot.save(update_fields=['capacity'])
    
    return JsonResponse({'status': 'success'}, status=200)
    

@csrf_exempt
def cancel_reservation(request):
    data = json.loads(request.body)
    reservation_id = data.get('reservation_id')
    
    reservation = Reservations.objects.get(id=reservation_id)
    reservation.status = Reservations.CANCELED
    reservation.save(update_fields=['status'])
    
    time_slot = reservation.time_slot
    time_slot.capacity += int(reservation.head_count)
    time_slot.save(update_fields=['capacity'])
    
    return JsonResponse({'status': 'success'}, status=200)
    
@csrf_exempt
def cancel_order(request):
    # find by id and change status, 
    # find user refund reward
    data = json.loads(request.body)
    order_id = data.get('order_id')
    
    order = OrderHistory.objects.get(id=order_id)
    order.status = OrderHistory.CANCELED
    order.save(update_fields=['status'])
    
    user = order.username
    user.reward_points -= float(order.reward_change)
    user.save(update_fields=['reward_points'])
    
    return JsonResponse({'status': 'success'}, status=200)



# def menu(request):
#     items = Menu.objects.all().values()
#     return JsonResponse(list(items), safe=False)

@csrf_exempt
def place_order(request):
    data = json.loads(request.body)

    ## get item ordered, username
    item_ordered = data.get("cart")
    reward_change = data.get("reward")
    username = data.get('username')

    ## update reward
    user = LoginCredentials.objects.get(username=username)
    user.reward_points += float(reward_change)
    user.save(update_fields=['reward_points'])

    ## add to order history
    order = OrderHistory.objects.create(
        username=user,
        items_ordered=item_ordered,
        reward_change=reward_change,
        status=OrderHistory.IN_PROGRESS
    )
    order.save()

    return JsonResponse({'status': 'success', 'message': 'Order placed successfully'}, status=200)

@csrf_exempt
def update_cart(request):
    data = json.loads(request.body)
    username = data.get('email')
    cart = data.get('cart')
    user = LoginCredentials.objects.get(username=username)
    user.shopping_cart = cart
    user.save(update_fields=['shopping_cart'])
    return JsonResponse({'message': 'Cart updated successfully'}, status=200)


def reset_data(request):
    AvailableTimeSlots.objects.all().delete()
    LoginCredentials.objects.all().delete()
    Reservations.objects.all().delete()
    OrderHistory.objects.all().delete()
    
    user = LoginCredentials.objects.create(
        username="admin@123.com",
        password=make_password("123456"),
    )
    user.save()
    
    
    
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=30)

    meal_times = [
        ('breakfast', 10),
        ('lunch', 10),
        ('dinner', 10),
    ]

    time_slots = []

    current_date = start_date
    while current_date <= end_date:
        for meal, capacity in meal_times:
            time_slots.append(
                AvailableTimeSlots(date=current_date, meal=meal, capacity=capacity)
            )
        current_date += datetime.timedelta(days=1)

    AvailableTimeSlots.objects.bulk_create(time_slots)

    return JsonResponse({'status': 'success', 'message': 'Time slots generated successfully'})


