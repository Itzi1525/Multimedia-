import struct
import hashlib
import random
import math

def leer_bmp(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    offset = struct.unpack_from('<I', data, 10)[0]
    width  = struct.unpack_from('<i', data, 18)[0]
    height = struct.unpack_from('<i', data, 22)[0]
    row_size = (width * 3 + 3) & ~3

    header = bytearray(data[:offset])
    pixels = bytearray(data[offset:])

    return header, pixels, width, height, row_size


def guardar_bmp(filepath, header, pixels):
    with open(filepath, 'wb') as f:
        f.write(header)
        f.write(pixels)


def derivar_clave(password: str, length: int) -> bytes:
    hash_bytes = hashlib.sha256(password.encode()).digest()
    clave = bytearray()

    while len(clave) < length:
        clave.extend(hash_bytes)

    return bytes(clave[:length])

def cifrar_xor(mensaje: bytes, password: str) -> bytes:
    clave = derivar_clave(password, len(mensaje))
    return bytes(m ^ k for m, k in zip(mensaje, clave))


def descifrar_xor(cifrado: bytes, password: str) -> bytes:
    return cifrar_xor(cifrado, password)  # XOR es simétrico



def generar_permutacion(password: str, total_bytes: int):
    seed = int(hashlib.sha256(password.encode()).hexdigest(), 16)
    random.seed(seed)

    posiciones = list(range(total_bytes))
    random.shuffle(posiciones)

    return posiciones



def embed_secure(src_path, dst_path, mensaje, password):
    header, pixels, width, height, row_size = leer_bmp(src_path)

    msg_bytes = mensaje.encode('utf-8')
    msg_cifrado = cifrar_xor(msg_bytes, password)

    msg_len = len(msg_cifrado)

    datos = struct.pack('>I', msg_len) + msg_cifrado

    bits = []
    for byte in datos:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    if len(bits) > len(pixels):
        raise ValueError("Mensaje demasiado grande para esta imagen")

    perm = generar_permutacion(password, len(pixels))

    pixels_mod = bytearray(pixels)

    for i, bit in enumerate(bits):
        pos = perm[i]
        pixels_mod[pos] = (pixels_mod[pos] & 0xFE) | bit

    guardar_bmp(dst_path, header, pixels_mod)

    print(f"[OK] {msg_len} bytes cifrados e incrustados en {dst_path}")


def extract_secure(stego_path, password):
    _, pixels, _, _, _ = leer_bmp(stego_path)

    perm = generar_permutacion(password, len(pixels))


    len_bits = [pixels[perm[i]] & 1 for i in range(32)]

    msg_len = 0
    for b in len_bits:
        msg_len = (msg_len << 1) | b

    total_bits = 32 + msg_len * 8

    if total_bits > len(pixels):
        raise ValueError("Contraseña incorrecta o datos corruptos")

    msg_bits = [pixels[perm[i]] & 1 for i in range(32, total_bits)]

    msg_bytes = bytearray()

    for i in range(0, len(msg_bits), 8):
        byte = 0
        for bit in msg_bits[i:i+8]:
            byte = (byte << 1) | bit
        msg_bytes.append(byte)

    msg_descifrado = descifrar_xor(bytes(msg_bytes), password)

    return msg_descifrado.decode('utf-8')




MENSAJE = "TELEMÁTICA SECRETA 2025"
CLAVE   = "clave_super_segura"

embed_secure("imagen.bmp", "stego_seguro.bmp", MENSAJE, CLAVE)

recuperado = extract_secure("stego_seguro.bmp", CLAVE)

print("Mensaje recuperado:", recuperado)

assert recuperado == MENSAJE
print("Prueba exitosa ")