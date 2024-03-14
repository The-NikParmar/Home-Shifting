from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import razorpay
from django.conf import settings

# Create your views here.
def home(request):
    return render(request,'home.html')


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
                        # t_packagetype = request.POST['package_type'],
                        # t_packageprice = request.POST['package_price'],
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
    return render(request,'tcontact.html')

def login(request):
    if request.POST:
        print(">>>>>>>>>>>>>>>>>page loade login")
        try:
            truckpartner = Truckpartner.objects.get(t_email = request.POST['email'] , t_password = request.POST['pass'])
            request.session['temail']=truckpartner.t_email
            request.session['tpassword']=truckpartner.t_password
            request.session['tname']=truckpartner.t_name
            request.session['tpicture'] = truckpartner.t_picture.url
            request.session['tcontact'] = truckpartner.t_contact
            
            print(">>>>>>>>>session start : ",request.session['temail'])
            msg1 = "login succesfully done"
            messages.success(request,msg1)
            # packages = Package.objects.filter(truck = truckpartner)
            # if packages.razorpay_order_id:
            return render(request,"home.html")
        except: 
            msg="Your email or password is not match !!!!"
            messages.error(request,msg)
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def logout(request):
    del request.session['temail']
    del request.session['tpassword']
    del request.session['tname']
    del request.session['tpicture']
    del request.session['tcontact']
    return redirect("tsignup")

def Mywallet(request):
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
    return render(request,'profile.html',{"truckpartner":truckpartner})

def Withdrawal_funds(request):
    return render(request,'Withdrawal_funds.html')
"""def packages(request):
    if request.POST:
        try:
            truckpartner = Truckpartner.objects.get(t_email = request.POST['email'])
            if truckpartner:
                price = int(request.POST.get("price"))
                pacakge = Package.objects.create(
                    package_name = request.POST['ptype'],
                    price = price
                )
                client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
                payment = client.order.create({'amount': pacakge.price * 100, 'currency': 'INR', 'payment_capture': 1})
                pacakge.razorpay_order_id = payment['id']  
                pacakge.save()

                context = {
                        'payment': payment,
                        'pacakge':pacakge,  # Ensure the amount is in paise
                    }
                
                print("=======================",context)
                print("&7777777777777777777777",payment)
                return render(request,'payments.html',context)
            else:
                return redirect('tsignup')
        except Exception as e:
            price(e)
            return redirect('tsignup')

    else:
        return render(request,'packages.html')
"""

def packages(request):
    if request.POST:
        try:
            truck =Truckpartner.objects.get(t_email = request.POST['temail'])

            price = int(request.POST.get('price'))
            
            truck.price = price
            truck.package_type = request.POST['ptype']
            truck.truck_type = request.POST['vtype']
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

        truck.razorpay_payment_id = request.GET.get('razorpay_payment_id')

        print('========================================',truck.razorpay_payment_id)
        truck.save()
        return render(request, 'tsuccess.html')
    except Exception as e:
        print(e)
        return render(request, 'tsuccess.html')