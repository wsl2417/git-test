import requests
import json
from ks_mini.request_send.user_account import global_token
url = "https://trade-testing.casamiel.cn/Pad/v3/Delivery/GetDetail"

payload = json.dumps({
   "orderCode": "E231124162326472566",
   "token": "e5a7a6aa3b8149459ec192fe7144365a"
})
headers = {
   'Authorization': 'Bearer {token}',
   'token': global_token,
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

