1 - STEGANO : Well hidden message#1: insignificant blue

Description du défi :

On a USB key marked with the seal of the Black Mist, a mysterious film was discovered. This film, that you are watching from the  EIGHTH ROW  of seats in the Cogswell Halls cinema, shows apparently innocuous scènes. But according to rumors, it is not just a simple video. Data would have been compressed and hidden there… 

Format: You need to find bytes of a zip archive containing the flag HACKDAY{FLAG}
SHA256: f950cd9690cefea88deb08af718c8933ded7641758ed145724d7812ee79102d0

Résolution :
Une archive zip est cachée dans les pixels des images de cette vidéo. 
Le fichier vidéo n'est pas compressé. Il faut extraire chaque image et effectuer un filtre LSB sur la couleur bleu et récupérer les 8 premières lignes. les 8 lignes de chaque images doivent être concaténé puis chaque bloc doit être concaténé dans l'ordre. Ca reforme le code binaire de l'archive zip
Le flag est a l'intérieur de l'archive avec les fichiers qui servent a l'étape 2 et 3.

FLAG:
HACKDAY{s73@M_$7@tion_4CcE5S}