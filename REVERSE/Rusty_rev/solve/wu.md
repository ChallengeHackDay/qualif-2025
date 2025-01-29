# Partie 1
Dans un premier temps, on peut voir qu'on a 2 fichiers qui sont inclus dans le binaire (pendant la compilation)
```rust
let enc_bytes = include_bytes!("mal.bin");
let key = include_bytes!("key");
```
On trouve key = 0xe023 2c75 9eeb dd98 6224 8411 6e94 8e5e 0a

Ensuite, on voit qu'on appelle une fonction comme :
```rust
let mal = decrypt(enc_bytes, key, BLOCK_SIZE);
```
On peut remarquer qu'on décrypte `enc_bytes` avec `key`
```rust
fn decrypt(bytes: &[u8], key: &[u8; 16], block_size: usize) -> Vec<u8> {
    let key = GenericArray::from(*key);
    let cipher = Aes128::new(&key);

    let mut decrypted = Vec::new();
    for block in bytes.chunks(block_size) {
        let mut block_array = GenericArray::clone_from_slice(block);
        cipher.decrypt_block(&mut block_array);
        decrypted.extend_from_slice(&block_array);
    }

    // Unpad the decrypted bytes
    let padding_size = *decrypted.last().unwrap() as usize;
    decrypted = (decrypted[..decrypted.len() - padding_size]).to_vec();

    decrypted
}
```

Puis on appelle la fonction `fileless_exec`
```rust
fn fileless_exec(payload: Vec<u8>) {
    let empty = CString::new("").unwrap();
    let p_filename = empty.as_c_str();

    let fd = memfd_create(p_filename, MemFdCreateFlag::MFD_CLOEXEC).unwrap();

    unistd::write(&fd, &payload).unwrap();

    let env = CString::new("").unwrap();
    let arg = CString::new("").unwrap();

    fexecve(fd.as_raw_fd(), &[&arg], &[&env]).unwrap();
}
```
Qui crée un fichier temporaire dans la RAM avec `memfd_create`, puis l'exécute avec `fexecve`.

Pour passer à la suite, il faut décrypter la fonction afin de trouver le stade final du challenge (j'ai mis le stade finale dans le drive)

# Partie 2
Il y a des fonctions anti debugging : 
- si il y a un PID (autre que 0) dans la ligne `TracerPid` du fichier `/proc/self/status`, roll un chiffre aléatoire entre 1 et 4
- si on a le 1, change la clé (qu'on verra plus tard) par `ST0P17`
- si on a le 2, print un amongus et quitte
- si on a le 3, print `gdb error, please reboot the computer` puis quitte
- si on a le 4, print `ggwp, you can validate using this password` après que l'user ait entré son mdp sans vérifier le mot de passe (attention donc c'est pas parce qu'on a ce message que le flag est trouvé)

On a une variable `key = "5734M3D"` (sauf dans le cas 4 de la fonction anti debug).

Ensuite on nous demande un mot de passe.
On itère ensuite sur les bytes de `key` (avec key qui cycle si l'input est plus long que la clé) et de guess en même temps, puis on appelle la fonction `calculate` avec les deux éléments, et enfin on met le résultat dans `out`.
```rust
let out: Vec<u8> = guess
	 .trim()
	 .bytes()
	 .zip(key.cycle())
	 .map(|(x1, x2)| calculate(x1, x2))
	 .collect();
```
La fonction `calculate` fait, sans les instruction inutiles, ce calcul `(x1.rotate_left(3) ^ x1) ^ (x2.rotate_right(1) ^ x2)`

On compare ensuite out avec `[165, 231, 243, 63, 141, 225, 245, 15, 202, 27, 18, 101, 15, 225, 5, 34, 15, 207, 20, 54, 232, 60, 58]`.
Pour trouver le mot de passe, il nous suffit d'inverser le calcul, ce qui nous donne `HACKDAY{D0N7_637_rU57Y}`