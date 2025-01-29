# **Challenge : "A mistake"** 

**Catégorie** : Forensic. 
## **Énoncé complet** 

It turns out that before leaving on vacation, he had actually tried to manualy falsify his username... Could he be less innocent than he seems?

Try to uncover his old username (old modification) !

-----------------------

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
7. Comme on sait qu'il à essayé de modifier à la main, la méthode la plus simple est de chercher des différences entre les fichiers de conf et de sauvegarde de conf : ``diff /mnt/etc/group /mnt/etc/group-` 

FORMAT FLAG : HACKDAY{username}
FLAG : HACKDAY{4nc1eNI0gin}