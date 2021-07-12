import io
from ext2 import file
from PIL import Image


ext2file = file.File()

ext2file.read("data/", "agwc.txt")

ext2file.print_statistics()


# Extract agwc.jpg from ext2file

first_inode_index = ext2file.super_block.s_first_ino  # Get block index of first inode
first_inode = ext2file.inodes[first_inode_index]  # Get first inode via their block index

data_blocks = ext2file.get_inode_blocks(first_inode)  # Get data blocks from first inode

img = Image.open(io.BytesIO(data_blocks))  # Save bytes from data_blocks into image file
img.save("data/agwc.jpg")  # Save image file at path/name
