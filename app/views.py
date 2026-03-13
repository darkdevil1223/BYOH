from django.shortcuts import render,HttpResponse


from django.shortcuts import render, redirect
from .models import ServerRequest

# OAuth Configuration
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from authlib.integrations.django_client import OAuth

# OAuth Configuration
CONF_URL = 'https://sso.iitb.ac.in/.well-known/openid-configuration'

oauth = OAuth()
oauth.register(
    name='hpc',
    client_id='cchpcaccreq',
    client_secret='gY5el0C5nW2Lh5XNqLGKeKm0oY9Os8P1Vk3nOvOWAzWn5MVZZM',
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid'}
)

# Home View (Displays User Information)
# def home(request):
#     user = request.session.get('user')
#     if user:
#         user = json.dumps(user, indent=2)
#     return render(request, 'index.html', context={'user': user})

# Login View (Redirects to OAuth Provider)
def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))  # Set the redirect URI to the auth view
    state = os.urandom(32).hex()
    nonce = os.urandom(32).hex()
    
    # Store state and nonce in session for later validation
    request.session['state'] = state
    request.session['nonce'] = nonce
    
    # Redirect to the authorization page
    return oauth.hpc.authorize_redirect(request, redirect_uri, state=state, nonce=nonce)

# Authentication Callback View (Handles OAuth Callback)
# Authentication Callback View
def auth(request):
    try:
        token = oauth.hpc.authorize_access_token(request)
            #newmade
        user_info = token.get('userinfo')
        if user_info:
            request.session['user'] = user_info
            # request.session['user_email'] = user_info['email']
        else:
            return HttpResponse("Failed to fetch user information.", status=400)
    except Exception as e:
        return HttpResponse(f"Authentication error: {e}", status=500)
    
    # Redirect directly to index.html after successful authentication
    
    # return redirect('existinguser')
    return redirect('index')


# Logout View (Logs User Out)
# Logout View (Logs User Out and Clears Session)
def logout(request):
    # Clear the user session data
    request.session.pop('user', None)
    request.session.pop('state', None)
    request.session.pop('nonce', None)
    request.session.pop('form_data', None)
    request.session.pop('group_members', None)
    
    # Redirect to the index page (or any other page you want after logout)
    return redirect('landing')




########################## code for exiting user #########################

def existinguser(request):


    # ldap_id = request.session.get('ldap_id')  # Fetch LDAP ID from session

    user_info = request.session['user']
    ldap_id = user_info['sub']
    
    if request.method == "POST":
        ldap_id = request.POST.get("ldap_id")  # Get LDAP ID from the form
        request.session["ldap_id"] = ldap_id  # Store in session

    # If LDAP ID exists and user is found in the database, redirect to 'existing_user.html'
    if ldap_id and UserRequest.objects.filter(ldap_id=ldap_id).exists():
        return redirect(existing_user)

    # Otherwise, redirect to 'index.html'
    return redirect(index)

    return render(request, 'existinguser.html')



def index(request):
    if request.method == "POST":
        ServerRequest.objects.create(
            full_name=request.POST.get('full_name'),
            ldap=request.POST.get('ldap'),
            department=request.POST.get('department'),
            extension_number=request.POST.get('extension_number'),
            server_name=request.POST.get('server_name'),
            number_of_servers=request.POST.get('number_of_servers'),
            rack_space_units=request.POST.get('rack_space_units'),
            power_per_server=request.POST.get('power_per_server'),
            cpu_gpu_details=request.POST.get('cpu_gpu_details'),
        )
        return redirect('success')

    return render(request, 'index.html')


def success(request):
    return render(request, 'success.html')

def landing(request):
    user = request.session.get('user')
    if user:
        user = json.dumps(user, indent=2)
    return render(request, 'landing.html', context={'user': user})

