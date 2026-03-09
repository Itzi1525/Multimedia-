from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

mp3_path = r"C:\Users\YOGA THINKPAD X1\OneDrive - Instituto Politecnico Nacional\Attachments\Documents\Multimedia\Beat Take 1.mp3"


image_path = r"C:\Users\YOGA THINKPAD X1\OneDrive - Instituto Politecnico Nacional\Attachments\Documents\Multimedia\Imagen2.jpg"

audio = MP3(mp3_path, ID3=ID3)

if audio.tags is None:
    audio.add_tags()

audio.tags.delall("APIC")

with open(image_path, "rb") as img:
    audio.tags.add(
        APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=img.read()
        )
    )

audio.save()

print("La portada fue reemplazada correctamente")