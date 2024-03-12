from django.db import models
from myapp.models import *
# Create your models here.

class Truckpartner(models.Model):
	user = models.ForeignKey(User,on_delete =models.CASCADE ,null=True)
	booking = models.ForeignKey(Booking,on_delete = models.CASCADE,null=True)
	t_name = models.CharField(max_length = 30)
	t_email = models.EmailField(unique=True , max_length = 30)
	t_password = models.CharField(max_length = 20)
	t_contact = models.CharField(max_length = 11 , unique = True)
	t_rcnumber = models.CharField(max_length = 50 , unique = True)
	t_aadharcard_details = models.CharField(max_length = 30 , unique = True)
	t_pancard_details = models.CharField(max_length = 30 , unique = True)
	t_drivinglicence_details = models.CharField(max_length = 30 , unique = True)
	t_picture = models.ImageField(upload_to="images/" ,default="images/pic-1.jpg")
	def _str_(self):
	    return self.t_name + " || " + self.t_contact    	