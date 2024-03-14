from django.db import models
from myapp.models import *
from django.utils import timezone
from datetime import timedelta
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

	#====================================================================================
	package_type = models.CharField(max_length=20,null=True)
	price = models.PositiveIntegerField(null=True)
	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(null = True)
	truck_type = models.CharField(max_length=20,null = True)
		
	def __str__(self):
		return self.t_name
	
	