"""
Google Sign-In Authentication

Endpoint: POST /api/auth/google
Body: { "id_token": "<google-id-token>" }

Verifies the token using google-auth, then finds or creates a `User` record
and returns the user object.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse

import google.auth.transport.requests
import google.oauth2.id_token
import requests
import json
from fastapi.responses import HTMLResponse
from app.config import settings

router = APIRouter()

class TokenRequest(BaseModel):
    id_token: str


@router.post("/google", response_model=UserResponse)
def google_sign_in(request: TokenRequest, db: Session = Depends(get_db)):
    """Verify Google ID token and return/create user"""
    if not request.id_token:
        raise HTTPException(status_code=400, detail="id_token is required")

    try:
        # Verify the token
        request_adapter = google.auth.transport.requests.Request()
        id_info = google.oauth2.id_token.verify_oauth2_token(request.id_token, request_adapter)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid ID token")

    # Extract user info
    email = id_info.get("email")
    name = id_info.get("name") or id_info.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Google token did not contain an email")

    # Find or create user
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return db_user

    new_user = User(email=email, full_name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/google/callback", response_class=HTMLResponse)
def google_callback(code: str = None, db: Session = Depends(get_db)):
    """OAuth2 redirect callback: exchange code for tokens, verify id_token, create user and return an HTML page that stores the user to localStorage and redirects to frontend."""
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in callback")

    # Exchange authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        resp = requests.post(token_url, data=payload)
        resp.raise_for_status()
        tokens = resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Token exchange failed: {str(e)}")

    id_token = tokens.get("id_token")
    if not id_token:
        raise HTTPException(status_code=400, detail="No id_token returned by Google")

    try:
        request_adapter = google.auth.transport.requests.Request()
        id_info = google.oauth2.id_token.verify_oauth2_token(id_token, request_adapter, settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid ID token")

    email = id_info.get("email")
    name = id_info.get("name") or id_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google token did not contain an email")

    # Find or create user
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        db_user = User(email=email, full_name=name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # Return a small HTML page that stores the user in localStorage and redirects
    # to the frontend app. This avoids the frontend having to call the backend again.
        user_json = {
                "id": db_user.id,
                "email": db_user.email,
                "full_name": db_user.full_name,
                "is_active": db_user.is_active
        }

        # Dump as JSON so JS receives valid literals (true/null) instead of Python's True/None
        user_json_str = json.dumps(user_json)

        frontend = settings.FRONTEND_URL.rstrip('/')
        # Store JSON as a string literal in localStorage so frontend can JSON.parse it
        html = f"""
        <!doctype html>
        <html>
            <head>
                <meta charset="utf-8" />
                <title>Signing you in...</title>
            </head>
            <body>
                <script>
                    try {{
                        // Insert JSON string into localStorage
                        localStorage.setItem('ims_user', '{user_json_str}');
                    }} catch (e) {{ console.error(e); }}
                    window.location.href = '{frontend}';
                </script>
                <p>If you are not redirected, <a href="{frontend}">click here</a>.</p>
            </body>
        </html>
        """

        return HTMLResponse(content=html, status_code=200)
