To Do the social media authentication with google and facebook then follow the below steps.
create developer accounts in the facebook and google developer consoles.
Add client_id and client_secret in urls.py 
google_client_id = ""
google_client_secret = ""
google_redirect_uri = "http://127.0.0.1:8000/auth"

fb_client_id = ""
fb_client_secret = ""
fb_redirect_uri = "http://127.0.0.1:8000/callback/facebook"

if you change redirect url makesure that you are adding the same in the urls.py also.

run the manage.py and open localhost:8000/google for google and localhost:8000/fb for facebook.
