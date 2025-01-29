3 - Well hidden message#3 : Standard Code Encryption

Description du défi :

The notes you have discovered hold a secret. They contain a text coded using a process that the monk seems to have devised himself. However, the Black Mist hackers have introduced a subtlety: they have adapted this method to the basic language of machines.

Format: HACKDAY{flag}


Instruction :
On repart des fichiers de l'archive de l'étape 1.
Utilisez la méthode de Trithemius (nom de la personne de l'étape 2) adaptée à la table ASCII (standard) pour décrypter le message. 
chiffrage : (char + i)%127 avec char qui est le code ascii du caractère, i qui est sa position.
déchiffrage : (char -i)%127

FLAG:
HACKDAY{8rUmE_NOIR3_H!DD3N_Ch@mb3R}