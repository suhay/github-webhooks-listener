import hmac
import hashlib
import os
import sys


async def auth(header, data):
    token = os.environ.get("API_TOKEN")
    tokenb = bytes(token, 'utf-8')

    signature = 'sha256=' + hmac.new(tokenb, data, hashlib.sha256).hexdigest()
    if hmac.compare_digest(signature, header):
        return True
    return False


if __name__ == "__main__":
    if len(sys.argv) == 3:
        body = sys.argv[1]
        header = sys.argv[2]
        if auth(header, body):
            print('true')
        else:
            print('false')
    elif len(sys.argv) == 2:
        body = sys.argv[0]
        header = sys.argv[1]
        if auth(header, body):
            print('true')
        else:
            print('false')
    else:
        print('false')
