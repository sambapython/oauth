"""oauth_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import requests
from django.urls import path
from django.http import HttpResponseRedirect, HttpResponse
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

google_client_id = ""
google_client_secret = ""
google_redirect_uri = "http://127.0.0.1:8000/auth"

fb_client_id = ""
fb_client_secret = ""
fb_redirect_uri = "http://localhost:8000/callback/facebook"
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def googlelogin(request):
	token_request_uri = "https://accounts.google.com/o/oauth2/auth"
	response_type = "code"
	scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
	url = f"{token_request_uri}?response_type={response_type}&client_id={google_client_id}&redirect_uri={google_redirect_uri}&scope={scope}"
	#resp = requests.get(url)
	return HttpResponseRedirect(url)

def googleauth(request):
	code=request.GET.get('code')
	access_token_uri = 'https://accounts.google.com/o/oauth2/token'
	resp = requests.post(access_token_uri, json={
		'code':code,
		'redirect_uri':google_redirect_uri,
		'client_id':google_client_id,
		'client_secret':google_client_secret,
		'grant_type':'authorization_code'
	})
	token_data = resp.json().get("access_token")
	print("*"*100)
	print(token_data)
	resp = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={token_data}")
	user_data = resp.json()
	username = user_data.get("email")
	return HttpResponse(username)

def fblogin(request):
	authorization_base_url = 'https://www.facebook.com/dialog/oauth'
	
	facebook = OAuth2Session(fb_client_id, redirect_uri=fb_redirect_uri)
	facebook = facebook_compliance_fix(facebook)
	authorization_url, state = facebook.authorization_url(authorization_base_url)
	return HttpResponseRedirect(authorization_url)

def fbauth(request):
	redirect_response = request.GET.get("code")
	facebook = OAuth2Session(fb_client_id, redirect_uri=fb_redirect_uri)
	facebook = facebook_compliance_fix(facebook)
	token_url = 'https://graph.facebook.com/oauth/access_token'
	token = facebook.fetch_token(token_url, client_secret=fb_client_secret,
                      code=redirect_response)
	print("*" * 100)
	access_token = token.get("access_token")
	resp = requests.get('https://graph.facebook.com/me?access_token=%s'%access_token)
	return HttpResponse(resp.content)
	



urlpatterns = [
    path('admin/', admin.site.urls),
    path("google/",googlelogin),
    path("auth/",googleauth),
    path("fb/",fblogin),
    path("callback/facebook/",fbauth),
]
