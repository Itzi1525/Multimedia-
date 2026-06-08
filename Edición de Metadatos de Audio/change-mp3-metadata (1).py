from mutagen.id3 import ID3, TIT2, TPE1, TALB
from mutagen.mp3 import MP3

# Path to your MP3 file
file_path = r"C:\Users\YOGA THINKPAD X1\OneDrive - Instituto Politecnico Nacional\Attachments\Documents\Multimedia\Beat Take 1.mp3"

# Load the MP3 file
audio = MP3(file_path, ID3=ID3)

# Modify metadata (e.g., Title, Artist, Album)
audio.tags.add(TIT2(encoding=3, text="Beat Take 1"))   # Title
audio.tags.add(TPE1(encoding=3, text="The Neighbourhood"))  # Artist
audio.tags.add(TALB(encoding=3, text="Hard To Imagine The Neighbourhood Ever Changing"))   # Album

# Save changes
audio.save()

print("Metadata updated successfully!")
