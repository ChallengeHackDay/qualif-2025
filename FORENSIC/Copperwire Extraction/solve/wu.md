# The Copper Wire Extraction
<p align="justify">This challenge was a forensic one, in which data had been exfiltrated over network. The goal was to retreived the files that had been exfiltrated. To do so a single network capture was provided. </p>

<p align="center">
<img src="Screenshots/S4.png" style="width: 50%">
</p>

<p align="justify"> Looking at the protocol hierarchy in Wireshark, it appeared that the data had been exfiltrated over only one protocol, namely HTTP. Especially over HTTP cookies as shown on the snippet below. Indeed files data seemed to be distributed and base64 encoded over cookie, in each request : </p>

<p align="center">
<img src="Screenshots/S2.png" style="width: 50%">
</p>

<p align="justify">To retreive files extracted, it was important to understand what type of files had been exfiltrated. To do so the very first packet extracted revealed very helpful because it could have contained some magic bytes : </p>

<p align="center">
<img src="Screenshots/S3.png" style="width: 50%">
</p>

<p align="justify">Indeed it was the case insofar as the first cookie, once decoded, revealed PNG magic bytes, meaning that the files that were supposed to be retreived were actually PNGs : </p>

````text
89 50 4e 47 0d 0a 1a 0a
````

So the final steps to get the flag were :

- Filtering the capture file to retreive all the base64 cookies
- Base64 decoding the amount of data, deleting all \r and \n, and gathering all the bytes in a single binary file
- Parsing binary file with PNG magic bytes
- Extracting PNGs

<p align="justify"> To do so, commands below were helpful (for some reasons Wireshark added, during exfiltration, a '=' infront of each cookie; which had to be removed to extract properly PNGs. It can explain the regex with sed)  : </p>

````bash
tshark -r file.pcapng -Y "http.request" -T fields -e http.cookie > flagb64
sed 's/^=//' flagb64 > flagb64_withoutpadding
tr -d '\n' < flagb64_withoutpadding > flagb64_1line
cat flagb64_1line | base64 -d > flag.bin
./PNG_extractor.py flag.bin
````

<p align="justify"> To parse the binary file and retreive PNGs, I implemented a tiny python script available under PNG_extractor.py in this repo. Finally after running previous commands, 17 numbered PNGs had been retreived, corresponding to the 17 chars of the flag: </p>

FLAG : _HACKDAY{D4t4_Exf1Ltr@t10n}_
