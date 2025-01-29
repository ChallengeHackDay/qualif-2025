import cv2
import numpy as np

def extract_data_from_frame(frame, width):

    #Separate colors
    b, _, _ = cv2.split(frame)

    #Get 8 firsts lines
    flat_blue = b[:8, :].flatten()

    #Extract LSB
    extracted_bits = [str(pixel & 1) for pixel in flat_blue]

    #Group to bytes
    binary_data = ''.join(extracted_bits[:width * 8])
    byte_data = [int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8)]

    return bytearray(byte_data)



#Get video
cap = cv2.VideoCapture("Train.avi" )

#Get video size
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

extracted_data = bytearray()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #Get fram data
    frame_data = extract_data_from_frame(frame, width)

    #Stop if a full fram is 0
    if all(byte == 0 for byte in frame_data):
        break

    extracted_data.extend(frame_data)

cap.release()

#Create zip
with open("extracted_archive.zip", "wb") as f:
    f.write(extracted_data)