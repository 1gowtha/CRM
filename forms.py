from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User   # django default user model
class OrderForm(ModelForm): # name of the model and Form. and inherit from ModelForm.
    class Meta:
        model = Order # which model
        fields = '__all__' # which fields i will allow - ['customer', 'product']. but i take here all.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
from django.contrib.auth.models import Group
user = User.objects.get(username='2300032467')
admin_group = Group.objects.get(name='admin')
admin_group.user_set.add(user)
from django.contrib.auth.models import User
try:
    user = User.objects.get(username='2300032467')
except User.DoesNotExist:
    user = None

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
   class Meta:
        model = Feedback
        fields = ['name', 'email', 'phone', 'comments']