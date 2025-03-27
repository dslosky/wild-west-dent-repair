from fastapi import FastAPI, Request, Response
from mangum import Mangum

from models import ContactModel, SettingsModel
from send_email import send_new_contact_email

settings = SettingsModel()
app = FastAPI()

# Salt to your taste
ALLOWED_ORIGINS = '*'

# handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'

    if not settings.PROD:
        response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'

    if not settings.PROD:
        response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    return response

@app.post("/contact")
def post_contact(
    contact: ContactModel
):
    print(f"We have contact!\n{contact}")
    send_new_contact_email(
        contact.name, contact.email, contact.phone, contact.message
    )

    return {"result": "success"}

handler = Mangum(app)
