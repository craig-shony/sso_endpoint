from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
import jwt, re, time
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from sqlalchemy import true

app = Flask(__name__)

#set up keys for JWT signing
public_key = open('.ssh/id_rsa.pub', 'r').read()
key = serialization.load_ssh_public_key(public_key.encode())

#set up limiter for rate limiting
limiter = Limiter(app, key_func=get_remote_address)

def isSso(arg):
    if arg == 'sso':
        return True
    else:
        return False

def isParsley(email):
    regex = r'\b[A-Za-z0-9._%+-]+@parsleyhealth+\.com\b'
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

def timeStamp():
    ts = int(time.time())
    return ts


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # decoding the payload to fetch the stored details
            jwt.decode(token, key=key, algorithms=['RS256', ])
        except:
            return jsonify({
                'message': 'Unable to verfiy'
            }), 401
        # returns the current logged in users contex to the routes
        return f(*args, **kwargs)

    return decorated


@app.route("/sso", methods=['POST'])
#rate limit can be increased based on estimated usage from senior-parsley app
@limiter.limit("10/minute")
@token_required
def endpoint():
    token = request.headers['x-access-token']
    data = jwt.decode(jwt=token, key=key, algorithms=['RS256', ])

    if (timeStamp() - data['expiry']) < 3600:

        if isSso(data['auth-provider']) and isParsley(data['email']):
            return {"sso":['verified']}
        else:
            return jsonify({
                    'message': 'Could not verify'
                }), 401
    else:
        return jsonify({
                'message': 'Token expired'
            }), 401
