from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=40)
    uemail = models.EmailField()
    ucontact = models.CharField(max_length=15)
    upassword = models.CharField(max_length=40)
    

    def __str__(self):
        return  self.uname + " || " + self.uemail   