# **Challenge : "What was I doing"**


**Catégorie** : Forensic.

## **Énoncé complet**

Edgar would like you to determine what he was doing just before leaving. According to his memory, he was conducting research, but on what...?
Checkout what the user was researching before he left.

------------------------

Do not run it as a VM it'll change files inside !

sha256: bbd71d5e0435d0abc75d3b969318605bced8ffd847064a65ca9d930769bf61cf
## Réalisation

plusieurs méthodes possibles dont :

1. Récupérer le fichier .qcow2
2. Installer qemu-utils : `sudo apt install qemu-utils`
3. Charger le module NBD : `sudo modprobe nbd`
4. On connecte ensuite le fichier .qcow2 à un périférique nbd : ` sudo qemu-nbd --connect=/dev/nbd0 /chemin/vers/le/fichier.qcow2
5. Check le montage : `sudo lsblk`
6. Une fois la partition identifié la monter : `sudo mount /dev/nbd0p1 /mnt
7. Afficher l'état dans lequel était firefox : 
   ` cat /mnt/home/test/.mozilla/firefox/xtet5yft.default-esr/places.sqlite` 
   le flag se trouve dans le fichier.
   Possible de trouver avec Strings ou grep car le flag est directement au bon format.
   
FLAG : HACKDAY{htTPs://hAckD@y.fR/CHaL13nG3}