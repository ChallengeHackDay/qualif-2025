# Useless Animals Sorting Challenge Writeup

1. **Receive and Decode Images:**
   For each of the 100 images, the server will send a base64 encoded string representing the image. You need to decode this string to get the image bytes.

   ```python
   import base64
   base64_image = "..."  # The base64 string received from the server
   image_bytes = base64.b64decode(base64_image)
   ```

2. **Predict the Animal:**
   Use the provided model to predict the animal in the image. The model is embedded in the image exif metadata. Try manually to find the corresponding animals and binary values in the model field.

   ```python
   from exif import Image
   labels = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'horse', 'sheep', 'spider', 'squirrel']
   image = Image(image_bytes)
   predicted_animal = labels[int(image.get("model"), 2)]
   ```

## Example Script

Here is an example script to automate the process:

```python
import base64
from exif import Image
from pwn import remote

labels = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'horse', 'sheep', 'spider', 'squirrel']

def predict(base64_image):
    image_bytes = base64.b64decode(base64_image)
    image = Image(image_bytes)
    return labels[int(image.get("model"), 2)]

r = remote('remote', 1111)
r.recvuntil(b'start the game')
r.sendline(b'')
for i in range(100):
    s = r.recvline()
    if b"Image" not in s:
        print("output:", s)
        exit()
    base64_image = r.recvline().strip().decode()
    r.recvuntil(b'?')
    result = predict(base64_image)
    print("Image n°", i+1, ":", result)
    r.sendline(result.encode())
    r.recvline()
    r.recvline()
r.interactive()
```

## Conclusion

By following the steps outlined above, you should be able to successfully complete the Useless Animals Sorting challenge and obtain the flag. Good luck!