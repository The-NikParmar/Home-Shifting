from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from myapp.models import *
from myapp2.models import *
from django.contrib import messages
import razorpay
from django.conf import settings

# Create your views here.

def home(request):
    try:
        uemail = request.session.get('uemail')
        user = get_object_or_404(User, uemail=uemail)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
        print("===========-----------------------",booking.htype)
        truckpartner = Truckpartner.objects.get(t_email=request.session['temail'])
        print(truckpartner.package_type)
        if truckpartner.is_online == True:
            if booking.statuscheck == False:
                if booking.status != 'finish':
                    # uemail = request.session.get('email')
                    # user = get_object_or_404(User, uemail=uemail)
                    # booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
                    if booking.htype in ['2 BHK'] and truckpartner.package_type in ['Silver','Gold','Platinum']:
                        print("----------------")
                        return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner})
                    elif booking.htype in ['1 BHK'] and truckpartner.package_type in ['Silver', 'Platinum']:
                        return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
                    elif booking.htype in ['3 BHK'] and truckpartner.package_type in ['Gold', 'Platinum']:
                        return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
                    elif booking.htype in ['1 BHK', '2 BHK', '3 BHK', '4 BHK'] and truckpartner.package_type == 'Platinum':
                        return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
    except Exception as e:
        print("---------------",e)
    return render(request,"home.html")

def accept(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        
        uemail = request.session.get('uemail')
        user = get_object_or_404(User, uemail=uemail)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

        truckpartner.on_work = True
        truckpartner.save()

        booking.statuscheck = True
        booking.save()

        uemail = request.session.get('uemail')
        user = get_object_or_404(User, uemail=uemail)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
        print("------------------",booking.finish_active)
        return render(request,"accept.html",{'user':user , "booking":booking})
    except Exception as e:
        print('============---------------',e)
        pass
    return render(request,"home.html")
        
    
def reject(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
    truckpartner.on_work = False
    truckpartner.save()
    return redirect('thome')

def finishride(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
    truckpartner.on_work = False
    
    uemail = request.session.get('uemail')
    user = get_object_or_404(User, uemail=uemail)
    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
    booking.statuscheck = False
    booking.status = 'finish'
    truckpartner.save()
    booking.save()
    print("------------------------------",booking.finish_active)
    
    #--------------------------------------------------
    uemail = request.session.get('uemail')
    user = get_object_or_404(User, uemail=uemail)
    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

    # Check if the last ride was more than 24 hours ago
    ride = Rides.objects.get(truckpartner=truckpartner)

    print(ride)

    if ride.today_earning == 0:
        ride.start_time =  timezone.now()
        ride.expiry_time = ride.start_time + timedelta(days=1)
        ride.save()

    current_datetime = timezone.now()

    if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
        ride.today_earning = 0
        ride.save()

        # Update total_trip and total_earning
    ride.total_trip += 1
    ride.today_earning += booking.price
    ride.total_earning += booking.price
    ride.save()

    print("------------------------------",booking.finish_active)

    return redirect('thome')

def signup(request):
    if request.POST:
            try:
                print(">>>>>>>>>>>>>page loade")
                truckparner = Truckpartner.objects.get(t_email = request.POST['temail'])
                print(">>>>>>>>>>>truckparner",truckparner)
                messages.error(request,'Email alredy exists!!!')
                return redirect('tlogin')
                
            except:
                if request.POST['password'] == request.POST['cpassword']:
                    truckparner = Truckpartner.objects.create(
                        t_name=request.POST['name'],
                        t_email=request.POST['temail'],
                        t_password=request.POST['password'],
                        t_contact=request.POST['contact'],
                        t_rcnumber=request.POST['rcn'],
                        t_aadharcard_details=request.POST['adhaar'],
                        t_pancard_details=request.POST['pan'],
                        t_drivinglicence_details=request.POST['driving'],
                    )
                    print(">>>>>>user ",truckparner.t_name)
                    msg="Sign Up Successful"
                    messages.success(request,msg)
                    return redirect('pdetails')

                else:
                    msg1="Password and Confim Password Does Not Matched !!!"
                    messages.error(request,msg1)
                    return redirect('tsignup')
    else:
        return render(request,"tsignup.html")

def contact(request):
    if request.POST:
        contact = Contact.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            number = request.POST['number'],
            message = request.POST['msg']
        )
        contact.save()
        return render(request,'tcontact.html')
    else:
        return render(request,"tcontact.html")

def login(request):
    if request.POST:
        print(">>>>>>>>>>>>>>>>>page loade login")
        try:
            truckpartner = Truckpartner.objects.get(t_email = request.POST['email'] , t_password = request.POST['pass'])
            if truckpartner.razorpay_payment_id:
                request.session['temail']=truckpartner.t_email
                request.session['tpassword']=truckpartner.t_password
                request.session['tname']=truckpartner.t_name
                request.session['tpicture'] = truckpartner.t_picture.url
                request.session['tcontact'] = truckpartner.t_contact

                if truckpartner:
                    truckpartner.is_online = True
                    truckpartner.save()
                    print("===============is online ============")
            
                print(">>>>>>>>>session start : ",request.session['temail'])
                msg1 = "login succesfully done"
                messages.success(request,msg1)
                # packages = Package.objects.filter(truck = truckpartner)
                # if packages.razorpay_order_id:
                return render(request,"home.html")
            else:
                return redirect('pdetails') 
        except: 
            msg="Your email or password is not match !!!!"
            messages.error(request,msg)
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def logout(request):
    truckparner = Truckpartner.objects.get(t_email = request.session['temail'])
    if truckparner:
        truckparner.is_online = False
        truckparner.save()
        print("==========================this is offline ")
    del request.session['temail']
    del request.session['tpassword']
    del request.session['tname']
    del request.session['tpicture']
    del request.session['tcontact']
    return redirect("tsignup")

def Mywallet(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        ride = Rides.objects.get(truckpartner = truckpartner)
        print("============",ride)
        transactions = Transactions.objects.filter(truckpartner = truckpartner)
        a = 0
        for i in transactions:
            a += i.amount
        
        print("============",transactions)
        current_datetime = timezone.now()

        if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
            ride.today_earning = 0
            ride.save()

        return render(request,'Mywallet.html',{'ride':ride,'transactions':transactions,'a':a})
    except Exception as e:
        print(e)
        return render(request,'Mywallet.html')


def update(request):
    if request.POST:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        truckpartner.t_name = request.POST['name']
        truckpartner.t_contact = request.POST['number']
        if 'picture' in request.FILES:
            truckpartner.t_picture = request.FILES['picture']
        
        truckpartner.save()

        request.session['tname'] = truckpartner.t_name
        request.session['tpicture'] = truckpartner.t_picture.url
        request.session['tcontact'] = truckpartner.t_contact
        
        msg ="profile successfully update"
        messages.success(request,msg)
        return redirect('profile')
    else:
        return render(request,"update.html")

def profile(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
    ride = Rides.objects.get(truckpartner = truckpartner)
    current_datetime = timezone.now()
    if ride.expiry_time is not None:
        if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
            ride.today_earning = 0
            ride.save()
        print(ride.today_earning)
        return render(request,'profile.html',{"truckpartner":truckpartner , 'ride':ride})
    else:
        return render(request,'profile.html',{"truckpartner":truckpartner , 'ride':ride})

  
def Withdrawal_funds(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        ride = Rides.objects.get(truckpartner = truckpartner)

        if request.POST:
            print("==========post")
            if request.POST['accountno'] == request.POST["caccountno"]:
                print("==========first",type(ride.total_earning))
                print("==========first",type(request.POST["amount"]))
                if ride.total_earning >= int(request.POST["amount"]):
                    print("==========second")
                    transactions = Transactions.objects.create(
                        truckpartner = truckpartner,
                        rides = ride,
                        account_holder_name = request.POST['hname'],
                        account_number = request.POST['accountno'],
                        ifsc_code = request.POST['ifsc_code'],
                        amount = request.POST['amount'],
                    )

                    ride.total_earning -= int(request.POST["amount"])
                    ride.save()

                    return redirect('Mywallet')
                else:
                    msg="inficiunce Balance!!"
                    messages.error(request,msg)
                    return render(request,'Withdrawal_funds.html')
            else:
                msg="account number and confirm account number does not match !!"
                messages.error(request,msg)
                return render(request,'Withdrawal_funds.html')
        else:
            return render(request,'Withdrawal_funds.html')
        
    except Exception as e:
        print(e)
        return render(request,'Withdrawal_funds.html')

def packages(request):
    if request.POST:
        try:
            truck =Truckpartner.objects.get(t_email = request.POST['temail'])

            price = int(request.POST.get('price'))
            
            truck.price = price
            truck.package_type = request.POST['ptype']
            truck.truck_type = request.POST['vtype']
            truck.start_date = timezone.now().date()
            truck.end_date = truck.start_date + timezone.timedelta(days=30)
            print('==========truckprice',truck.price)

            #request.session['email'] = request.POST['email']

            client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': truck.price * 100, 'currency': 'INR', 'payment_capture': 1})
            truck.razorpay_order_id = payment['id']  
            truck.save()

            request.session['tpemail']= request.POST['temail']
            #print(p)
            context = {
                    'payment': payment,
                    'truck':truck,  # Ensure the amount is in paise
                }
            print(context)
        
            return render(request,'payments.html',context)

        except Exception as e:
            print(e)
            return render(request,"packages.html")
    else:
        return render(request,"packages.html")

def payments(request):
    #truck =Truckpartner.objects.get(t_email = request.POST['temail'])
    return render(request,"payments.html")

def pdetails(request):
    return render(request,"pdetails.html")

def tsuccess(request):
    try:
        truck = Truckpartner.objects.get(t_email = request.session['tpemail'])
        print('========================================',truck.t_email)


        truck.razorpay_payment_id= request.GET.get('razorpay_payment_id')
        print('========================================',truck.razorpay_payment_id)
        truck.save()

        ride = Rides.objects.create(

            truckpartner = truck
        
        )
        print("---------------create ride for truckpartners",ride)
        return render(request, 'tsuccess.html')
    
    except Exception as e:
        print(e)
        return render(request, 'tsuccess.html')
    
def changepassword(request):
    if request.POST:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        if truckpartner.t_password == request.POST["current_pass"]:
            if request.POST["new_pass"] == request.POST["c_pass"]:

                truckpartner.t_password = request.POST["new_pass"]
                truckpartner.save()

                del request.session['temail']
                del request.session['tpassword']
                del request.session['tname']
                del request.session['tpicture']
                del request.session['tcontact']
                return redirect('tsignup')
            else:
                msg = "new password and confirm password does not match !!"
                messages.error(request,msg)
                return render(request,'changepassword.html')
        else:
            msg = "current password does not match !!"
            messages.error(request,msg)
            return render(request,'changepassword.html')
    else:
        return render(request,'changepassword.html')