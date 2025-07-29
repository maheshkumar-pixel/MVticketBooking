from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Ticketbook ,TripPackage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_view')
        else:
            return render(request, 'login.html', {'error': "Invalid credentials"})
    return render(request, 'login.html')




@csrf_exempt  # Needed if you aren't sending the CSRF token correctly
@login_required
def submit_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            required_fields = ['name', 'source', 'destination', 'bus_type',
                               'ticket_amount', 'seat_number', 'select_date', 'select_time']

            if not all(field in data for field in required_fields):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            booking = Ticketbook.objects.create(
                user=request.user,
                name=data['name'],
                source=data['source'],
                destination=data['destination'],
                bus_type=data['bus_type'],
                ticket_amount=data['ticket_amount'],
                seat_number=data['seat_number'],
                select_date=data['select_date'],
                select_time=data['select_time'],
            )

            return JsonResponse({
                'status': 'success',
                'booking_id': booking.id,
                'redirect_url': '/success/'
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def book_ticket(request):
    return render(request, 'book_ticket.html')

@login_required

def home_view(request):
    return render(request, 'home.html')

@login_required
def success(request):
    return render(request, 'success.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Ticketbook, id=order_id, user=request.user)
    
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    
    return render(request, 'confirm_delete.html', {'order': order})

@login_required
def delete_package(request, package_id):
    package = get_object_or_404(TripPackage, id=package_id, cust_name=request.user.username)

    if request.method == 'POST':
        package.delete()
        return redirect('order_list')

    return render(request, 'confirm_delete.html', {'package': package})

@login_required
def order_list(request):
    orders = Ticketbook.objects.filter(user=request.user).order_by('-id')
    packages = TripPackage.objects.filter(cust_name=request.user.username).order_by('-id')  # Assuming cust_name == username

    return render(request, 'order_list.html', {
        'orders': orders,
        'packages': packages
    })


def submit_package(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            print("Received data:", data)

            # Extract data from the request
            
            cust_name = request.user.username  # ✅ Not from JSON

            package_name = data.get('name', 'Custom Package')
            amount = data.get('amount', 2500)
            duration = data.get('duration', 3)
            no_of_tickets=data.get('no_of_tickets',1)
            places = data.get('places', [])

            # Save to DB
            trip_package = TripPackage.objects.create(
                cust_name=cust_name,
                name=package_name,
                amount=amount,
                duration_days=duration,
                no_of_tickets=no_of_tickets,
                places=places  
            

            )

            

            # Return JSON response for AJAX or redirect for form submission
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Package created successfully',
                    'redirect_url': '/trip_package/'  # Add redirect URL for client-side
                })
            else:
                return redirect('trip_package')

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)

def trip_package(request):
    return render(request, 'trip_package.html')