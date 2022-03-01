import requests
from requests.structures import CaseInsensitiveDict
from jwt_generator import tokenGen


url = "http://localhost:5000/sso"

headers = CaseInsensitiveDict()
headers["appname"] = "senior-parsley"
headers["x-access-token"] = tokenGen(5)

data = ""


resp = requests.post(url, headers=headers, data=data)
print(resp.status_code, resp.json())