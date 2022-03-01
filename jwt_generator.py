import jwt, sys
from cryptography.hazmat.primitives import serialization
import time

private_key = open('.ssh/id_rsa', 'r').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=None)

payload_data = { "payload1" :
    {"auth-provider": "sso",
    "email": "test1@parsleyhealth.com"},
    "payload2" :
    {"auth-provider": "user-pass",
    "email": "test2@parsleyhealth.com"},
    "payload3" :
    {"auth-provider": "sso",
    "email": "test3@gmail.com"},
    "payload4" : {"auth-provider": "sso",
    "email": "test4@parsleyhealth.comm"}
}


def timeStamp():
    ts = int(time.time())
    timeStamp = {"expiry": ts}
    return timeStamp

def tokenGen(i):
    payload = ''
    if i > 0 and i < 5:
        pKey = "payload" + str(i)
        payload=payload_data[pKey]
        payload.update(timeStamp())
    elif i == 5:
        payload=payload_data['payload1']
        ts = (int(time.time())-5000)
        payload.update({"expiry": ts})
    else:
        print(str(i) + " is not a valid index")
        return -1
    


    new_token = jwt.encode(
        payload=payload,
        key=key,
        algorithm='RS256'
    )

    return new_token

if __name__ == "__main__":
    i = sys.argv[1]
    print(tokenGen(i))