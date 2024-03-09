from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')


def signup(request):
    if request.POST:
            try:
                print(">>>>>>>>>>>>>page loade")
                truckparner = Truckpartner.objects.get(t_email = request.POST['email'])
                print(">>>>>>>>>>>truckparner",truckparner)
                messages.error(request,'Email alredy exists!!!')
                return redirect('tlogin')
                
            except:
                if request.POST['password'] == request.POST['cpassword']:
                    truckparner = Truckpartner.objects.create(
                        t_name=request.POST['name'],
                        t_email=request.POST['email'],
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
                    return redirect('tlogin')

                else:
                    msg1="Password and Confim Password Does Not Matched !!!"
                    messages.error(request,msg1)
                    return redirect('tsignup')
    else:
        return render(request,"tsignup.html")

def contact(request):
    return render(request,'contact.html')

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
            return redirect('thome')
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
