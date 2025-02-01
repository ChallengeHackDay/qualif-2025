from PIL import Image
import struct
import pickle

# On the picture it's possible to see that diagonal bits where changed

# Returns a list of diagonals spaced with a given spacing

def get_spaced_diagonals(width, height, spacing=500):
    diagonals = []

    # Main diagonals (top left to bottom right)
    # Offset with spacing
    for d in range(-height + 1, width, spacing):
        diagonal = [(y, y - d) for y in range(height) if 0 <= y - d < width]
        diagonals.append(diagonal)

    # Secondary diagonals (top right to bottom left)
    # Offset with spacing
    for d in range(1, width + height, spacing):
        diagonal = [(y, d - y - 1) for y in range(height) if 0 <= d - y - 1 < width]
        diagonals.append(diagonal)

    return diagonals


# Fonction to extract hidden data in the lower significant bits
def extract_data_from_image(image_path):
    # Load image
    im = Image.open(image_path)
    r, g, b = im.split()

    # Recover red data
    r_data = list(r.getdata())

    # Lire la longueur du message (32 bits)
    binary_length = ''.join([str(r_data[i] & 1) for i in range(32)])
    message_length = int(binary_length, 2)

    print(f"Longueur du message extraite : {message_length} octets")

    # Vérifier si l'image contient suffisamment de pixels pour le message
    if len(r_data) < 32 + (message_length * 8):
        raise ValueError("L'image ne contient pas assez de pixels pour le message.")

    # Lire le message
    binary_message = ''.join([str(r_data[i + 32] & 1) for i in range(message_length * 8)])
    message_bytes = bytes([int(binary_message[i:i + 8], 2) for i in range(0, len(binary_message), 8)])

    return message_bytes






def get_spaced_diagonals(width, height, spacing=500):
    """Retourne une liste de diagonales espacées avec un espacement donné."""
    diagonals = []

    # Diagonales principales (haut gauche -> bas droit)
    for d in range(-height + 1, width, spacing):  # Décalage avec espacement
        diagonal = [(y, y - d) for y in range(height) if 0 <= y - d < width]
        diagonals.append(diagonal)

    # Diagonales secondaires (haut droit -> bas gauche)
    for d in range(1, width + height, spacing):  # Décalage avec espacement
        diagonal = [(y, d - y - 1) for y in range(height) if 0 <= d - y - 1 < width]
        diagonals.append(diagonal)

    return diagonals



# La valeur 359 pour déterminer l'espacement des diagonales est trouvé dans les info extraites dans les bits de poids faibles

def extract_data_from_spaced_diagonals(image_path, spacing=359):
    """Extrait les données cachées dans les MSB des diagonales espacées."""
    im = Image.open(image_path)
    width, height = im.size
    r, g, b = im.split()

    r_data = list(r.getdata())
    diagonals = get_spaced_diagonals(width, height, spacing)

    # Transformer les données rouges en une grille 2D
    r_data = [list(r_data[i * width:(i + 1) * width]) for i in range(height)]

    # Extraire les bits des diagonales espacées
    extracted_bits = []
    for diagonal in diagonals:
        for y, x in diagonal:
            # Extraire le bit de poids fort (MSB) du pixel
            bit = (r_data[y][x] >> 7) & 1
            extracted_bits.append(bit)

    # Lire la longueur du message à partir des 32 premiers bits
    binary_length = ''.join(map(str, extracted_bits[:32]))
    message_length = int(binary_length, 2)

    print(f"Longueur du message extraite : {message_length} octets")

    # Vérifier si le message est complet dans les bits extraits
    total_bits = 32 + (message_length * 8)
    if total_bits > len(extracted_bits):
        raise ValueError("L'image ne contient pas assez de données pour reconstituer le message.")

    # Extraire le message binaire
    binary_message = ''.join(map(str, extracted_bits[32:32 + (message_length * 8)]))

    # Convertir le message binaire en bytes
    message_bytes = bytes([int(binary_message[i:i + 8], 2) for i in range(0, len(binary_message), 8)])

    return message_bytes






# krbl.png represent a Red Jacket (flag of Frind Eve 1)

hidden_image_path = r"./Where_is_Eve_2/krbl.png"



# Extract data 1
extracted_info = extract_data_from_image(hidden_image_path)

# Désérialiser les métadonnées avec pickle
extracted_data = pickle.loads(extracted_info)

# Afficher les métadonnées extraites
print(f"Extracted Data : {extracted_data}")

# Extracted Data : {305: b'PhotoMaster', 315: b'E', 269: b'Jacket picture', 270: b'Red Jacket', 271: b'Canored EOSIS', 272: b'74.12', 306: b'2024:01:23 00:00:00', 40092: b'Price: 359\xc2\xa3'}



# Extract data 2
# Need to see if there is number for extracting the data hidden in diagonals

Message = extract_data_from_spaced_diagonals(hidden_image_path)
print(f"Hidden data : {Message}")

# Hidden data : b"\x05\x13\x01\x02R)+n\x01\x00\x1di''\xc12U\xed\xcc\x16\x01\x1a\x1a'\x03\x19\t\x01Y8o\x00=2:\x95ZP\xcf\xf37`qW@%3+J\x12p"


# Guessy time

# The lore tell us to look for the tools that is 'Canored EOSIS' and the version is also needed '74.12' that will be the keys
# The hint say its a XOR

# It's also possible to find the result with brute force it


Make = "Canored EOSIS"
Version = 74.12

key1 = Make.encode('utf-8')
key2 = struct.pack("d", Version)
final_key = key1 + key2

final_key = final_key * (len(Message) // len(final_key) + 1)
texte_dechiffre = bytes([b ^ final_key[i] for i, b in enumerate(Message)])
final_text = texte_dechiffre.decode('utf-8')
print("Final result :", final_text)