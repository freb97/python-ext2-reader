import io
from ext2 import file
from PIL import Image


ext2file = file.File()

ext2file.read("data/", "agwc.txt")

ext2file.print_statistics()

# img = Image.open(io.BytesIO(ext2file.data_blocks))
# img.save("data/out.jpg")
