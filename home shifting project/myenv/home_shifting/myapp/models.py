from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=40)
    uemail = models.EmailField()
    ucontact = models.CharField(max_length=15)
    upassword = models.CharField(max_length=40)
    
    

    def __str__(self):
        return  self.uname + " || " + self.uemail   
    


class Booking(models.Model):
    ORDERSTATUS = (("house-type","house-type"),("Booking","Booking"),("payment-status","payment-status"),("on-the-way","on-the-way"),("cancel","Cancle"),("finish","finish process"))
    htype = models.CharField(max_length=40,null=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    bname = models.CharField(max_length=40)
    movefrom = models.CharField(max_length=40)
    moveto = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    zipcode = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField()
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=20,choices = ORDERSTATUS,default="Booking")


    def __str__(self):
        return  self.bname + " || " + self.htype   
