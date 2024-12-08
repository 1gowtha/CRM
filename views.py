from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory ## multiple forms in forms
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm # django default form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # restricted user access
from .decorators import unauthenticated_user, allowed_users, admin_only # custom restricted and allowed user acces
from django.contrib.auth.models import Group # Django signal to associated user with group

# Create your views here.
@login_required(login_url='login')
@admin_only # if customer the redirect to user-page and if admin redirect to view_func
def home(request):
    last_five_orders = Order.objects.all().order_by('-date_created')[:5]
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'last_five_orders':last_five_orders,
        'orders':orders,
        'customers':customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@admin_only # if customer the redirect to user-page and if admin redirect to view_func
def allOrders(request):
    orders = Order.objects.all()
    context = {
        'orders':orders,
    }

    return render(request, 'accounts/all_orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'staff'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()  # order_set means customers child order from model fields
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter
    }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3) # Parent model and Child model. extra=3 means you will see three times form to place order 3 items together. You can use extra=10 or extra=5 as you wish.
    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # form = OrderForm(initial={'customer':customer}) # To see the customer in form, for which customer profile i viewd.

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order) # to get pre-field form

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # Update (instance) and Post
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/update_order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()  # Now UserCreationForm will replace by CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)  # Now UserCreationForm will replace by CreateUserForm
        if form.is_valid():
            user = form.save() # to associated user with group
            username = form.cleaned_data.get('username') # to associated user with group
            messages.success(request, 'Account was create for ' + username) # to associated user with group
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) # to check the user is in model/db or not.
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is Incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)

    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer # logged in user
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)
import openai

openai.api_key = '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'  # Replace with your actual API key

def get_bot_response(user_message):
    """Generate a response from the OpenAI model."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    return response['choices'][0]['message']['content']

def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        bot_response = get_bot_response(user_message)
        return JsonResponse({'response': bot_response})
# chatbot/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Example conversation-based responses
CONVERSATION_FLOW = {
    "hello": "Hi there! How can I assist you today?",
    "how are you": "I'm just a bot, but thank you for asking! How can I assist you?",
    "what can you do": "I can help you with information about products, orders, and customer support. What would you like to know?",
    "help": "Sure! How can I help you today?",
}

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            # Parse JSON body
            data = json.loads(request.body)
            user_message = data.get('message', '').strip().lower()

            # Handle different types of customer messages
            if user_message in CONVERSATION_FLOW:
                bot_response = CONVERSATION_FLOW[user_message]
            else:
                bot_response = "I'm not sure how to respond to that. Can you please rephrase or ask something else?"

            return JsonResponse({'response': bot_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
from .forms import FeedbackForm

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/confirmation.html')
    else:
        form = FeedbackForm()
    return render(request, 'accounts/feedback_form.html', {'form': form})
