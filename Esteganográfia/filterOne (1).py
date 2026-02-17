# Binary filter: 16 Colors

file = open('./images/volcan.bmp','rb')
fileo = open('./images/palo_de_rosabin.bmp','wb')
metadata = file.read(54)
fileo.write(metadata)

# --- TUS COLORES ---
palo_de_rosa1 = [0xF0,0xF0,0xFA]
palo_de_rosa2 = [0xE0,0xE0,0xF5]
palo_de_rosa3 = [0xD1,0xD1,0xF0]
palo_de_rosa4 = [0xC1,0xC1,0xEB]
palo_de_rosa5 = [0xB2,0xB2,0xE6]
palo_de_rosa6 = [0xA3,0xA3,0xE1]
palo_de_rosa7 = [0x93,0x93,0xDC]
palo_de_rosa8 = [0x84,0x84,0xD7]
palo_de_rosa9 = [0x74,0x74,0xD2]
palo_de_rosa10 = [0x65,0x65,0xCD]
palo_de_rosa11 = [0x56,0x56,0xC8]
palo_de_rosa12 = [0x46,0x46,0xC3]
palo_de_rosa13 = [0x3C,0x3C,0xB9]
palo_de_rosa14 = [0x37,0x37,0xA9]
palo_de_rosa15 = [0x32,0x32,0x9A]
palo_de_rosa16 = [0x2D,0x2D,0x8B]



# --- CORRECCIÓN 1: AGRUPAR ---
# Metemos tus variables en una lista para poder acceder por número (0 al 15)
# El orden importa: celeste1 será el índice 0, celeste16 el índice 15.
paleta = [
    palo_de_rosa1, palo_de_rosa2, palo_de_rosa3,palo_de_rosa4, palo_de_rosa5,
    palo_de_rosa6,palo_de_rosa7,palo_de_rosa8,palo_de_rosa9,palo_de_rosa10,
    palo_de_rosa11,palo_de_rosa12,palo_de_rosa13,palo_de_rosa14,palo_de_rosa15,
    palo_de_rosa16
]

file.seek(54,0)
no_pix = 0

# --- CORRECCIÓN 2: EL LÍMITE ---
# Esto está perfecto. Es el tamaño de cada "rebanada" del pastel.
limite = (pow(2, 24)-1)/16 

while(True):
    # --- CORRECCIÓN 3: LEER EL PÍXEL ---
    # Te faltaba leer los 3 bytes del píxel actual
    pixel_data = file.read(3)

    if(len(pixel_data) > 0):
        # Convertimos los 3 bytes a un número gigante
        valor_int = int.from_bytes(bytes(pixel_data), byteorder='little')
        
        # --- CORRECCIÓN 4: CÁLCULO DEL ÍNDICE ---
        # En lugar de usar 'match', calculamos qué posición de la lista toca.
        # Dividimos el valor del píxel entre el tamaño del límite.
        indice = int(valor_int / limite)
        
        # Seguridad: Si el cálculo da 16 (por ser el máximo valor posible), lo bajamos a 15
        if indice > 15:
            indice = 15
            
        # --- CORRECCIÓN 5: ESCRIBIR ---
        # Usamos el 'indice' para sacar el color correcto de la lista 'paleta'
        fileo.write(bytes(paleta[indice]))
        
        no_pix += 1
    else:
        break

print('No Pixels: '+str(no_pix))
file.close()
fileo.close()