from django.shortcuts import render
from Login_app.forms import UserForm, UserInfoForm
from Login_app.models import UserInfo
from django.contrib.auth.models import User
# --------------------------------------------------
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
# view for index page
def index(request):
    dict = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        # querry to get user info based on primary key id from User admin
        user_basic_info = User.objects.get(pk=user_id)
        # querry to get user info based on primary key id from UserInfo model
        # must use 'filter' and 'get'. otherwise user_more_info
        filter_user_info = UserInfo.objects.filter(user__pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        dict = {'user_basic_info':user_basic_info, 'user_more_info':user_more_info}
    return render(request, 'Login_app/index.html', context=dict)

# view for registration page
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            # model 1
            user = user_form.save()
            # converting plain password text into encripted password text by hashing
            user.set_password(user.password)
            # update and save encripted password
            user.save()

            # model 2
            # holding image file valid or not for upload by 'commit=False'
            user_info = user_info_form.save(commit=False)
            # creating one to one relation with admin --> user model    with user_info
            user_info.user = user
            # checking image file valid or not
            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']
            user_info.save()

            registered = True
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()
    dict = {'user_form':user_form, 'user_info_form':user_info_form, 'registered':registered}
    return render(request, 'Login_app/register.html', context=dict)


# view for login/logout page
# login page
def login_page(request):
    return render(request, 'Login_app/login.html', context={})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate
        user = authenticate(username=username, password=password)
        if user:
            # without active user can't login. by default all user active
            if user.is_active:
                login(request, user)
                # calling index page using name='index' by reversfunction
                # HttpResponseRedirect help to go to the index page with index url name
                return HttpResponseRedirect(reverse('Login_app:index'))
            else:
                return HttpResponse("Acount is not active!!!")
        else:
            return HttpResponse("Login Details are Wrong!!")
    else:
        return HttpResponseRedirect(reverse('Login_app:login_page'))

# logout page
# decorators --> '@login_required' checking user login or not. if login the user can logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:index'))
