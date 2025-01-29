#!/usr/bin/python3

#import
import base64
import sys

#Functions 
def PNG_Extractor(f):
    PNG_MagicBytes = b'\x89PNG\r\n\x1a\n'
    PNG_EndBytes = b'IEND\xae\x42\x60\x82'
    p = 0
    PNG_count = 0
    
    with open(f,'rb') as file:
    	d = file.read()
    
    while True:
    	header_index = d.find(PNG_MagicBytes, p)
    	if header_index == -1:
            break
    	eof_index = d.find(PNG_EndBytes, header_index)
    	if eof_index == -1:
            break
    	png_data = d[header_index:eof_index + len(PNG_EndBytes)]
    	
    	output= f"Flag{PNG_count}.png"
    	
    	with open(output, 'wb') as output_file:
    		output_file.write(png_data)
    	print(f"[+] PNG #{PNG_count + 1} had been extracted {output}")
    	p = eof_index
    	PNG_count += 1
        
    if PNG_count == 0:
        print("No PNG file detected, based on Magic Bytes.")
    else:
        print(f"{PNG_count} PNG files had been detected and extracted successfully.")

#main
if __name__ == "__main__":
	if len(sys.argv) != 2:
        	print("Usage: python script.py <binary file to parse> ")
	else:
    		PNG_Extractor(sys.argv[1])
















