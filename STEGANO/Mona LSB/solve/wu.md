Python script to extract :

```python
with wave.open(input_file, 'rb') as audio:
    frames = bytearray(audio.readframes(audio.getnframes()))

midpoint = len(frames) // 2

lsb_bits = []
for i in range(midpoint, len(frames), interval):
    lsb_bits.append(str(frames[i] & 1))

binary_message = ''.join(lsb_bits)
extracted_message = ''.join(
    chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)
)

extracted_message = extracted_message.split('\x00', 1)[0]
return extracted_message

except Exception as e:
return f"An error occurred: {e}"
```


A lot of people were looking at pair frames, and other already had the flag but forgot to search it.
The flag was hidden in the middle of the file, so you had to grep or CTRL F to find it.