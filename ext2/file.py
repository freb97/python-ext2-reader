from ext2 import groupdescriptor
from ext2 import superblock


class File(object):
    def __init__(self):
        self.super_block = None
        self.group_descriptor = None

    def read(self, file_path):
        data = open(file_path, "rb").read()

        self.super_block = superblock.SuperBlock(data)
        self.group_descriptor = groupdescriptor.GroupDescriptor(data)

    def getSuperBlock(self):
        return self.super_block

    def getGroupDescriptor(self):
        return self.group_descriptor
