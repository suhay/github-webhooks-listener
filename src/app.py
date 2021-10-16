from auth import auth
from parse import parse
from quart import Quart, request


app = Quart(__name__)


@app.route('/webhooks/<repo>', methods=['GET', 'POST'])
async def webhooks(repo):
    if request.is_json:
        if 'X-Hub-Signature-256' in request.headers.keys():
            data = await request.data
            header = request.headers['X-Hub-Signature-256'].split('=')[1]
            if auth(header, data):
                payload = await request.get_json()
                parse(repo, payload)
                return 'Thanks!', 202
            else:
                return 'Signature is wrong...', 401
        else:
            return 'Signature is wrong...', 401

    else:
        return 'Not sure what this is...', 418


@app.errorhandler(404)
def page_not_found(e):
    return "?", 404


if __name__ == "__main__":
    app.run()
