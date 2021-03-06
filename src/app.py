from quart import Quart, request

from dotenv import load_dotenv
load_dotenv()

from release import processRelease
from multiprocessing import Process

import os
import hashlib
import hmac


token = os.environ.get("API_TOKEN")
tokenb = bytes(token, 'utf-8')

app = Quart(__name__)

@app.route('/webhooks/<repo>', methods=['GET','POST'])
async def webhooks(repo):
    if request.is_json:
      data = await request.data
      signature = hmac.new(tokenb, data, hashlib.sha1).hexdigest()

      if 'X-Hub-Signature' in request.headers.keys() and hmac.compare_digest(signature, request.headers['X-Hub-Signature'].split('=')[1]):
        payload = await request.get_json()

        if payload['repository']['name'] == repo and 'action' in payload.keys():
          if payload['action'] == 'released' and 'release' in payload.keys():
            p = Process(target=processRelease, args=(repo,payload))
            print(p.pid)
            p.start()

        return 'Thanks!', 202

      else:
        return 'Signature is wrong...', 401

    else:
      return 'Not sure what this is...', 418

@app.errorhandler(404)
def page_not_found(e):
    return "?", 404

if __name__ == "__main__":
    app.run()