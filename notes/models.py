from django.db import models
from django.contrib.auth.models import User
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_dat = models.DateTimeField(auto_now_add=True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
