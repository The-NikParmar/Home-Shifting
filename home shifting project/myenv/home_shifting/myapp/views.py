from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
import requests
from django.conf import settings
from django.urls import reverse
import razorpay


# Create your views here.


def index (request):
    return render(request,'index.html')

def signup(request):
    if request.POST:
        print(">>>>>>>>>>>page lode")
        try:
           print("=================Email Alredy exits===================")
           user = User.objects.get(uemail = request.POST['uemail'])
           print(">>>>>>>>>>>>>>>>Email Alredy Exist!!!!")
           msg1 = "email Alredy Exist !!!!!"
           messages.error(request,msg1)
           return redirect('index')
        except:
            if request.POST['upassword'] == request.POST['ucpassword']:
                user = User.objects.create(
                    uname = request.POST['uname'],
                    uemail = request.POST['uemail'],
                    ucontact = request.POST['ucontact'],
                    upassword = request.POST['upassword'],
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
            print("check password and email")
            user=authenticate=User.objects.get(uemail = request.POST['uemail'],upassword = request.POST['upassword'])
            request.session['uemail'] = user.uemail
            request.session['uname'] = user.uname
            request.session['upassword'] = user.upassword
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
    del request.session['upassword']
    print(">>>>>>>>>>>>>>>>>>>>>>>>LOGOUT")
    msg="Logout successfully"
    messages.success(request,msg)
    return redirect('index')

def change_pswd(request): 
   if request.POST:
       print("page lode")
       user=User.objects.get(uemail=request.session['uemail'])
       
       if user.upassword == request.POST['cu_password']:
           print("<<<<page lode user cureent password perfect >>>>>>")

           if request.POST['npassword'] == request.POST['cpassword']:
               print("========Page Loade new password and conifrm password match =========")
               user.upassword = request.POST['cpassword']
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
    if request.POST:
        try:
            print("====================================page loade =======================================")
            user = User.objects.get(ucontact = request.POST['ucontact'])
            mobile = request.POST['ucontact']
            otp = random.randint(1000,9999)
            print(type(otp))

            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {
                           "authorization":"49df8FP3OhnqKAuB6OcTLAAEMmfB23tmRFHiDFZRZ7zrpONWyuhl6B3wFteN",
                           "variables_values":str(otp),
                           "route":"otp",
                           "numbers":mobile
                        }

            headers = {
                'cache-control': "no-cache"
               }

            response = requests.request("GET", url, headers=headers, params=querystring)
            msg = "Otp Sent Successfully.........."
            print(msg)
            print(response.text)
            request.session['mobile']=mobile
            request.session['otp']=otp
            return render(request,'otp.html')
        except Exception as e:
                print(e)
                print("===========except page loade==============")
                msg = "invalid Phone Number  !!!"
                return render(request,"forget_pswd.html")
    else:
        print("==============================else part run ====================================")
        return render(request,"forget_pswd.html")
    
def otp(request):
    if request.method=="POST":     
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        print(type(otp))
        print(type(uotp))
        
        if otp==uotp:
          print("Hello")
          del request.session['otp']
          return render(request,"resetpass.html")
        else:
          msg = "Invalid Otp"
          print(msg)
          messages.error(request,msg)
          return render(request,"otp.html")
    else:
        return render(request,"otp.html")
    
def resetpass(request):
     print("=========== resetpage page hello===============")
     if request.POST:
         print("=========== request page hello===============")
         try:
            print("===========hello===============")
            user = User.objects.get(ucontact = request.session['mobile'])
            if request.POST['npassword']==request.POST['cnpassword']:
                print("===========1  hello===============")
                user.upassword =request.POST['npassword']
                user.save()
                return  redirect('index')
            else:
                pass
         except  Exception as e:
             print(e)
     else: 
         return render(request,'resetpass.html')
       
def booking(request):
    if 'uemail' in request.session:
        if request.POST:
            userid = User.objects.get(uemail=request.session['uemail'])
            price = int(request.POST.get('price'))
            book = Booking.objects.create(
                htype=request.POST['htype'],
                userid=userid,
                bname=request.POST['name'],
                movefrom=request.POST['moving_from'],
                moveto=request.POST['moving_to'],
                state=request.POST['state'],
                zipcode=request.POST['zipcode'],
                price=price
            )
            
            print(type(book.price))
            print("=================================")
    
            client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': book.price * 100, 'currency': 'INR', 'payment_capture': 1})
            book.razorpay_order_id = payment['id']
            book.save()

            context = {
                    'payment': payment,
                    'book':book,  # Ensure the amount is in paise
                }
            
            print("=======================",context)
            print("&7777777777777777777777",payment)


        
            return render(request, 'payment.html',context)
        else:
            return render(request, "booking.html")
    else:
        messages.info(request, "Please login now.........")
        return render(request, "booking.html")


def payments(request):
    return render (request,"payment.html")


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        try:
            # Verify the Razorpay payment
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            }
            client.utility.verify_payment_signature(params_dict)
            
            # Update the booking status or perform any other necessary actions
            booking = Booking.objects.get(razorpay_order_id=razorpay_order_id)
            booking.paid = True 
            booking.save()

            return HttpResponse("Payment successful")
        except Exception as e:
            # Handle verification failure or other exceptions
            print("Payment verification failed:", str(e))
            return HttpResponse("Payment verification failed")
    else:
        return HttpResponse("Invalid request method")



def vehical (request):  
    return render(request,'vehical.html')

def service (request):
    return render(request,'service.html')

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")


def dilevry_partners(request):
    return render(request,"dilevry_partners.html")

