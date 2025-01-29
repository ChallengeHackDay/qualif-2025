# **Challenge : "distracted user"**


**Catégorie** : Forensic.

## **Énoncé complet**

Inspector Edgar is one of the heads of the London police force. He’s caught many criminals, though he’s never quite understood how he managed to do it. In truth, he’s a bit clumsy and naïve, but not malicious in the slightest.

Right before going on vacation, he jotted down his password on a scrap of paper. Upon returning, he tried to log in but, being a bit absent-minded, he forgot his username. Not the best situation for logging in, is it?

Come on, give him a hand and look at the snapshot!

----------------------

Do not run it as a VM it'll change files inside !

sha256: bbd71d5e0435d0abc75d3b969318605bced8ffd847064a65ca9d930769bf61cf

flag format : HACKDAY{username}
## Réalisation

plusieurs méthodes possibles dont :

1. Récupérer le fichier .qcow2
2. Installer qemu-utils : `sudo apt install qemu-utils`
3. Charger le module NBD : `sudo modprobe nbd`
4. On connecte ensuite le fichier .qcow2 à un périférique nbd : ` sudo qemu-nbd --connect=/dev/nbd0 /chemin/vers/le/fichier.qcow2
5. Check le montage : `sudo lsblk`
6. Une fois la partition identifié la monter : `sudo mount /dev/nbd0p1 /mnt
7. Deux options sont à explorer : 
	1. Trouver le nom de l'utilisateur via le nom de la home (peut ne pas être fiable ou ne pas exister ce qui est d'ailleurs le cas).
	2. Aller dans le fichier etc/shadow et trouver l'utilisateur.

FORMAT FLAG : HACKDAY{username}
FLAG : HACKDAY{u$Erh4cKdAYF0rENsiCnIV1}