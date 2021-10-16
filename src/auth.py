import hmac
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("API_TOKEN")
tokenb = bytes(token, 'utf-8')


async def auth(header, data):
    signature = 'sha256=' + hmac.new(tokenb, data, hashlib.sha256).hexdigest()
    if hmac.compare_digest(signature, header):
        return True
    return False
