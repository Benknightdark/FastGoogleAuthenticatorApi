from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from starlette.requests import Request
import pyotp

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class OtpModel(BaseModel):
    username: str
    issuer_name: str
    secret_key: Optional[str]


@app.get("/", response_class=HTMLResponse)
def http(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/otp_uri", summary="回傳Google Authenticator驗證網址")
async def get_otp_uri(data: OtpModel):
    """
    回傳Google Authenticator驗證網址

    Args:
        data (OtpModel): Request Body

    Returns:
        json: 回傳Google Authenticator驗證網址
    """
    new_secret_key = ''
    print(data)
    if data.secret_key == None:
        new_secret_key = pyotp.random_base32()
    else:
        if data.secret_key == "":
            new_secret_key = pyotp.random_base32()
        else:
            new_secret_key = data.secret_key
    totp = pyotp.totp.TOTP(new_secret_key)
    provisioning_uri = totp.provisioning_uri(
        name=data.username, issuer_name=data.issuer_name)
    return {'provisioningUri': provisioning_uri}
