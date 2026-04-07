import os
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from authlib.integrations.django_client import OAuth
from .models import ServerRequest
from .ldap import fetch_ldap_user_data
# ================= OAuth Config =================

CONF_URL = 'https://sso.iitb.ac.in/.well-known/openid-configuration'

oauth = OAuth()
oauth.register(
    name='hpc',
    client_id='cchpcaccreq',
    client_secret='gY5el0C5nW2Lh5XNqLGKeKm0oY9Os8P1Vk3nOvOWAzWn5MVZZM',
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid email profile'}
)

# ================= Views =================

def landing(request):
    user = request.session.get('user')
    return render(request, 'landing.html', {
        'user': json.dumps(user, indent=2) if user else None
    })


def login(request):
    redirect_uri = request.build_absolute_uri(reverse('auth'))

    state = os.urandom(32).hex()
    nonce = os.urandom(32).hex()

    request.session['state'] = state
    request.session['nonce'] = nonce

    return oauth.hpc.authorize_redirect(request, redirect_uri, state=state, nonce=nonce)


def auth(request):
    try:
        if request.GET.get('state') != request.session.get('state'):
            return HttpResponse("Invalid state", status=400)

        token = oauth.hpc.authorize_access_token(request)

        user_info = None

        # ✅ Correct usage (NO nonce)
        try:
            user_info = oauth.hpc.parse_id_token(request, token)
        except Exception:
            pass

        # Fallback if needed
        if not user_info:
            userinfo_endpoint = oauth.hpc.server_metadata.get('userinfo_endpoint')
            if userinfo_endpoint:
                resp = oauth.hpc.get(userinfo_endpoint, token=token)
                if resp.ok:
                    user_info = resp.json()

        if not user_info:
            return HttpResponse("Failed to fetch user info", status=400)

        request.session['user'] = dict(user_info)

    except Exception as e:
        return HttpResponse(f"Authentication error: {e}", status=500)

    return redirect('index')


def logout(request):
    request.session.flush()
    return redirect('landing')


# ================= Server Request Flow =================
def index(request):
    if 'user' not in request.session:
        return redirect('login')

    user_info = request.session['user']

    # ✅ Extract from SSO
    ldap_id = user_info.get('sub', '')
    full_name = user_info.get('gecos', '') or user_info.get('name', '')
    department = user_info.get('departmentnumber', '')
    email = user_info.get('mail', '')

    if request.method == 'POST':
        # ✅ Directly save to DB
        ServerRequest.objects.create(
            full_name=request.POST.get('full_name', full_name),
            ldap=request.POST.get('ldap', ldap_id),
            department=request.POST.get('department', department),
            email=request.POST.get('email', email),
            extension_number=request.POST.get('extension_number', ''),
            server_name=request.POST.get('server_name', ''),
            number_of_servers=int(request.POST.get('number_of_servers', 0)),
            rack_space_units=int(request.POST.get('rack_space_units', 0)),
            power_per_server=float(request.POST.get('power_per_server', 0)),
            cpu_gpu_details=request.POST.get('cpu_gpu_details', ''),
        )

        return redirect('success')

    # ✅ Auto-fill form
    form_data = {
        'full_name': full_name,
        'ldap': ldap_id,
        'department': department,
        'email': email,
    }

    return render(request, 'index.html', {'form_data': form_data})

def success(request):
    return render(request, 'success.html')

