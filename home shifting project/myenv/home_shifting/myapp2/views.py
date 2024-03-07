from django.shortcuts import render


# Create your views here.
def partner_index(request):
     return render(request,'partner_index.html')

def profile(request):
     return render(request,'profile.html')

def Mywallet(request):
     return render(request,'Mywallet.html')

def dcontact(request):
     return render(request,'dcontact.html')

def withdrawal_funds(request):
     return render(request,'withdrawal_funds.html')

def update(request):
     return render(request,'update.html')

def plogin(request):
     return render(request,'plogin.html')