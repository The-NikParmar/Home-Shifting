from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random

# Create your views here.


def index (request):
    return render(request,'index.html')

def signup(request):
    if request.POST:
        print(">>>>>>>>>>>page lode")
        try:
            user = User.objects.get(uemail = request.POST['uemail'])
            print(">>>>>>>>>>>>> User object : ", user)
            messages.error(request, msg1)
            msg1="Email Already Exist !!!"
            return redirect('index')
        
        except:
            if request.POST['upassword'] == request.POST['ucpassword']:
                user = User.objects.create(
                    uname = request.POST['uname'],
                    uemail = request.POST['uemail'],
                    ucontact = request.POST['ucontact'],
                    upassword = request.POST['upassword'],
                    ucpassword = request.POST['ucpassword'],
                )
                print(user.uname)
                msg = "Your Registration Done ...."
                print("============",msg)
                messages.success(request, msg)
                return redirect('index')
                # add ragistration than redirect login page
            else:
                pmsg="Password and Confim Password Does Not Matched !!!"
                messages.error(request, pmsg)
                return redirect('index')
    else:
        return redirect('index')
    
def login(request):
    if request.POST:
        try:
            user=authenticate=User.objects.get(uemail = request.POST['uemail'],ucpassword=request.POST['ucpassword'])
            request.session['uemail'] = user.uemail
            request.session['uname'] = user.uname
            request.session['ucpassword'] = user.upassword
            print(">>>>>>>>>session start : ",request.session['uemail'])
            print(">>>>>>>>>>>> login successfully >>>>>>>>>>>>>>>>>...")
            msg = "login successfully"
            messages.success(request,msg)
            return redirect('index')  
        except: 
            msg="Your email or password is not match !!!!"
            messages.error(request,msg)
            print(msg)
            return redirect('index')
    else:
        return render(request,'index.html')
    
def logout(request):
    del request.session['uemail']
    del request.session['uname']
    del request.session['ucpassword']
    print(">>>>>>>>>>>>>>>>>>>>>>>>LOGOUT")
    msg="Logout successfully"
    messages.success(request,msg)
    return redirect('index')

def change_pswd(request): 
   if request.POST:
       print("page lode")
       user=User.objects.get(uemail=request.session['uemail'])
       
       if user.ucpassword == request.POST['cu_password']:
           print("<<<<page lode user cureent password perfect >>>>>>")

           if request.POST['npassword'] == request.POST['cpassword']:
               print("========Page Loade new password and conifrm password match =========")
               user.ucpassword = request.POST['cpassword']
               user.save()
               return redirect('logout')
           else:
                msg = "New Password conifrm  password Does not match..."
                messages.error(request,msg)
                return redirect('login')
       else:
           msg1="Current Password Does not match !!!"
           messages.error(request,msg1)
           return redirect('login') 
   else:
       return redirect('login')
   

def forget_pswd(request):
   pass
    
     
def booking (request):
    return render(request,'booking.html')

def vehical (request):  
    return render(request,'vehical.html')

def service (request):
    return render(request,'service.html')

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")
