from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import pyotp

app = FastAPI()


class OtpModel(BaseModel):
    username: str
    issuer_name: str
    secret_key: Optional[str]



@app.post("/otp_uri",summary="回傳Google Authenticator驗證網址")
async def get_otp_uri(data: OtpModel):
    """
    回傳Google Authenticator驗證網址

    Args:
        data (OtpModel): Request Body

    Returns:
        json: 回傳Google Authenticator驗證網址
    """
    new_secret_key = ''
    if data.secret_key == None:
        new_secret_key = pyotp.random_base32()
    else:
        new_secret_key = data.secret_key
    totp = pyotp.totp.TOTP(new_secret_key)
    provisioning_uri = totp.provisioning_uri(
        name=data.username, issuer_name=data.issuer_name)
    return {'provisioningUri': provisioning_uri}
