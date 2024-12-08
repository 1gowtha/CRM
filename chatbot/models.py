from django.db import models

# Create your models here.
from django.db import models

class ChatLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
