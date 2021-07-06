from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .forms import CreateUserForm, fileForm
from .models import file
from .djangoencryptfile import EncryptionService, ValidationError

# Create your views here.
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context={'form':form}
    return render(request, 'accounts/register.html',context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username  or  password is incorrect')
            
    #form=UserCreationForm()
    context={}
    return render(request, 'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def home(request):
    return render(request, 'accounts/dashboard.html')
@login_required(login_url='/login/')
def upload(request):
    context={}
    if request.method == 'POST':
        upload_file= request.FILES["document"]
        fs=FileSystemStorage()
        name=fs.save(upload_file.name, upload_file)
        context['url'] = fs.url(name)
    return render(request, 'accounts/upload.html',context)
@login_required(login_url='/login/')
def upload_file(request):
    if request.method == 'POST':
        form=fileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewfile')
    else:
        form=fileForm()
    return render(request, 'accounts/upload_file.html', {
        'form':form
    })
    
def delete_file(request, pk):
    if request.method == 'POST':
        files = file.objects.get(pk=pk)
        files.delete()
    return redirect('viewfile')

@login_required(login_url='/login/')
def sharefile(request):
    return render(request, 'accounts/sharefile.html')
@login_required(login_url='/login/')
def encrypt(request):
    return render(request, 'accounts/encrypt.html')
@login_required(login_url='/login/')
def decrypt(request):
    return render(request, 'accounts/decrypt.html')
@login_required(login_url='/login/')
def viewfile(request):
    files = file.objects.all()
    return render(request, 'accounts/viewfile.html',{
        'files':files
    })
@login_required(login_url='/login/')
def viewrequests(request):
    return render(request, 'accounts/viewrequests.html')
@login_required(login_url='/login/')
def downloadfile(request):
    return render(request, 'accounts/downloadfile.html')
def logout(request):
    return render(request, 'accounts/logout.html')
@login_required(login_url='/login/')
def encrypt_view(request):
   try:
       myfile = request.FILES.get('myfile', None)
       password = request.POST.get('password', None)
       encrypted_file = EncryptionService().encrypt_file(myfile, password, extension='enc')
       mymodel = MyModel.objects.create(uploaded_file=encrypted_file)
   except ValidationError as e:
       print(e)

def decrypt_view(request):
   try:
       my_object = MyModel.objects.get(pk=1)
       myfile = my_object.uploaded_file
       password = request.POST.get('password', None)

       decrypt_file = service.decrypt_file(encrypted_file, password, extension='enc')
       my_object.uploaded_file = decrypt_file
       my_object.save()
   except ValidationError as e:
       print(e)
