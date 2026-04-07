from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import uvicorn
import os

app = FastAPI()

# IMPORTANT: Change this to a random secret string
app.add_middleware(SessionMiddleware, secret_key="eShopCo-Secret-Key")

oauth = OAuth()
oauth.register(
    name='google',
    client_id='1091667072643-ok7f938tfefvl2kd67k6capmq092iq2h.apps.googleusercontent.com',
    client_secret='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',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get('/')
def home():
    return {
        "message": "Welcome to eShopCo Staff Portal",
        "instructions": "Go to /login to authenticate with Google",
        "login_url": "http://localhost:8000/login"
    }

@app.get('/login')
async def login(request: Request):
    # This must match one of the Authorized redirect URIs in Google Cloud Console
    redirect_uri = "http://localhost:8000/auth"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        # Store the raw id_token in the session
        request.session['id_token'] = token.get('id_token')
        return {
            "message": "Login successful!",
            "view_token": "http://localhost:8000/id_token"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get('/id_token')
async def get_id_token(request: Request):
    id_token = request.session.get('id_token')
    if not id_token:
        return {"error": "No id_token found. Please login at /login first."}
    return {"id_token": id_token}

if __name__ == "__main__":
    # Running on port 8000 as specified in the guide
    uvicorn.run(app, host="0.0.0.0", port=8000)
