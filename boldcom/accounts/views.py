# import email
from email.message import EmailMessage
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



# ========> Importing for email verification   <======== 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage ### note


from django.core.mail import send_mail
from django.conf import settings

from .tokens import account_activation_token

# Create your views here.

# ========> Register View <========
def register(request):
    if request.method == 'POST':
        # ===> this will contain all the field value
        form = RegistrationForm(request.POST)
        # ===> if the form is valid
        if form.is_valid():
            # ===> firstly we are fetching all the fields from the request 'POST'
            # ===> when we use django forms we have to use the 'cleaned_data' to fetch the values from the request
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # ===> we are creating the username base on the user email address 
            # ===> we want to take the some part from the email provided be the user
            username = email.split("@")[0]
            # ===> we want to create the user account
            # ===> the 'create_user' is from the django authentication model that we create in the model file
            user = Account.objects.create_user(first_name=first_name, 
                                               last_name=last_name, 
                                               email=email, 
                                               username=username, 
                                               password=password)
            user.phone_number = phone_number
            user.save()     
            
            # ========> User activation <========
            # ===> we are getting the current site, beacuse we are using the localhost
            current_site = get_current_site(request)
            # ===> we are taking the mail subject
            mail_subject = 'Please activate your account'
            # ===> we want to put the content we want to send in the email, i.e the template
            # ===> in the message we are taking the user object
            message      = render_to_string('accounts/account_verification_email.html', {
                # ===> this is the user object,
                # ===> in the verification email we want to tell the user that how about their account user.firstname.
                'user' : user,
                # 'domain' : current_site,
                'domain' : current_site.domain,  ## adams
                # ===> we are encoding this 'user.pk'  with ' urlsafe_base64_encode' so that nobody can see the primary key.
                # ===> we are also encoding the user primary key
                # ===> when we are activating the account we will decode it.
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                # ===> this 'default_token_generator.make_token' is the libery it has make.token and check.token functions, 'make_token ' will create a token of the user, it will create a token for the user.
                # ===> we are generatiing the token of that user                
                'token' : default_token_generator.make_token(user),
                # 'token' : account_activation_token.make_token(user),
            })
            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            
            # ===> 'success' is the success message
            messages.success(request, 'Thank you for registeriing with us we have sent you a verification on your email, please verify it.')
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)





# ========> Login View <========
def login(request):
    if request.method == 'POST':
        # ===> from the login form, the name values.
        email = request.POST['email']
        password = request.POST['password']
        
        # ===> will set the user so they can login
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'Your are now loggged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')






# ========> Logout View <========
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


# ========> Logout View <========
def activate(request, uidb64, token):
    
    
    '''
    # ===>  this ' urlsafe_base64_decode(uidb64).decode()' will decode the uidb,because we encoded it b4 we are now decoding it
    # ===> it will give us the primary key of the user 
    '''

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        '''
        # ===> this 'Account._default_manager.get(id=uid)' will return the user object
        '''
        user = Account._default_manager.get(id=uid)
        '''
        # ===> we are handling some errors
        # ===> if these or any of these error happens we are setting the user to none
        '''

    except(TypeError, ValueError, OverflowError, Account.DoesNotExists):
        user  = None
        
    # ===> we are checking the token
    # ===> if the error does not happen
    # ===> we want to take out the user from the token  ' check_token()'
    
    if  user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! your account is activated.')
        return redirect('login')

    else:
        messages.error(request,'Invalid activation link.')
        return redirect('register')