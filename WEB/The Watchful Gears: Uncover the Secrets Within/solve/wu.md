First, we saw a basic webpage containing an image.

By opening the image in a new tab, we could see the path to follow in the URL.

From there, we had access to an "index of" where another HTML page was located.

In this other HTML page, there was a form containing obfuscated JavaScript code. The flag was stored in one of the variables in the code, but it was encoded in base64 and divided into several parts.

We had to gather the parts in the correct order (indicated in another variable) and then decode it in base64.

Finally, there was a path to visit with another "index of" where the flag could be found.