# Resolution du challenge DLLception (de Glz_SQL)

---

### Les participants auront le fichier DLLception.dll

Cette dll est compilée en C# (.Net 6.0), il est donc possible de la décompiler avec un outils comme ILSpy

Après l'avoir décompilée une fois à la main (cf: dans l'interface graphique de ILSpy) le participant sera confronté à un gros code avec des appels de fonctions inutiles qu'il devra dans un premier temps nétoyer, déchiffrer le gros tableau de byte avec la clé et le vecteur présent dans les variables et le ré-écrire dans un fichier afin de l'analyser à nouveau avec ILSpy (car oui il s'agit encore une fois d'une autre DLL avec le même format mais un code différent (plus petit)). Car en effet, le paterne de code ce répète et cela 150 fois avant que le dernier code (la dernière dll) ne contienne le flag dans un char[] (au même titre que les poupée russes).


## Solution: 

Ma méthode à été de chercher à automatiser la décompilation et le déchiffrement de la dll et de la remplacer par le nouveau code tant qu'il n'y à pas d'erreur (tant que le paterne se répète).

PS: l'installation d'un module de décompilation en ligne de commande est plus pratique du style : ILSpycmd 

```python
import os, base64
from time import *

ts = time()
isError = False
cpt = 0
while not(isError):
    try:
        ts1 = time()
        os.system("ilspycmd.exe .\\dll.dll > _decompile.txt")

        code = open("_decompile.txt", "rb").read()

        bytearr = code.split(b"new byte[")[1:]
        print(len(bytearr))
        t = []
        for ba in bytearr:
            
            t.append(ba.split(b"{")[1].split(b"};")[0].replace(b"\r\n", b"").replace(b"\t", b""))

        Iv, Key = (bytes(eval("[" + str(t[0])[2:-1] + "]")), bytes(eval("[" + str(t[1])[2:-1] + "]")))
        
        print(Iv, Key)
        tab = eval("[" + str(t[2])[2:-1] + "]")

        open("dll.enc", "wb").write(bytes(tab))
        cpt += 1
        os.system(".\\decrypt.exe " + base64.b64encode(Key).decode() + " " + base64.b64encode(Iv).decode())
        print("[it] n*", cpt, "dll Length:", len(tab), "byte(s)", "round end in:", time() - ts1, "second(s).")
    except Exception as e:
        print(e)
        isError = True
dt = time() - ts

print("end in:", dt, "sec(s). N =", cpt, "iteration(s); speed:", dt / (cpt+1), "second(s) by step.")

```

Et pour le déchiffrement du binaire : 

```c#
using System;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;

namespace encrypt {
public class Program {
    public static void Main(string[] args) {
        if(args.Length < 2) {
            return;
        }

        byte[] data = File.ReadAllBytes("dll.enc");
        Aes aes = Aes.Create();
        aes.Mode = CipherMode.CBC;
        aes.Padding = PaddingMode.ISO10126;
        aes.Key = Convert.FromBase64String(args[0]);
        aes.IV = Convert.FromBase64String(args[1]);
        
        ICryptoTransform dict = aes.CreateDecryptor();
        byte[] dec = dict.TransformFinalBlock(data, 0, data.Length);
        
        

        File.WriteAllBytes("dll.dll", dec);
    }
}
}
```

Après décompilation finale, on obtient ça : 
<!> Attention spoil du flag.

---

```c#
using System;
using System.IO;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;

public class Program {
    
    public static void Main() {
        char[] fl4g = new char[56] { 'H', 'A', 'C', 'K', 'D', 'A', 'Y', '{', 'd', 'l', 'l', 'C', 'e', 'p', 't', 'i', 'o', 'n', '-', 'b', 'e', '9', '7', '4', '6', 'f', 'a', '-', 'd', '0', 'f', '7', '-', '4', '7', '6', '1', '-', 'a', '5', 'b', 'a', '-', '0', 'e', '4', '6', '1', 'a', '1', '6', '2', '8', '7', '7', '}' };
        System.Threading.Thread.Sleep(1);
        for(int i = 0; i < fl4g.Length; i++) {
            fl4g[i] ^= fl4g[i];
        }
        Console.WriteLine("Hello, World!");
    }
}
```