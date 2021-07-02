from ext2 import file

ext2file = file.File()

ext2file.read("data/agwc.txt")

superBlock = ext2file.getSuperBlock()
groupDescriptor = ext2file.getGroupDescriptor()
