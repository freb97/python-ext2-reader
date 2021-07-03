class Stats(object):
    def __init__(self, file):
        self.file_name = file.file_name

        self.block_size = str(file.super_block.s_log_block_size) + "bits"
        self.magic_number = str(hex(file.super_block.s_magic))

        self.creator_os = self.getCreatorOSName(file.super_block.s_creator_os)

        self.total_inodes = str(file.super_block.s_inodes_count)
        self.total_free_inodes = str(file.super_block.s_free_inodes_count)

        self.total_blocks = str(file.super_block.s_blocks_count)
        self.total_free_blocks = str(file.super_block.s_free_blocks_count)

    def toString(self):
        br = "\n"
        tab = "\t"

        output = "EXT2 File statistics for file \"" + self.file_name + "\":" + br + br

        output += "Block size:" + 8 * tab + self.block_size + br
        output += "Magic number (must equal 0xef53):" + 2 * tab + self.magic_number + br
        output += "Created on OS:" + 7 * tab + self.creator_os + br + br

        output += "Total inode count:" + 6 * tab + self.total_inodes + br
        output += "Total free inode count:" + 5 * tab + self.total_free_inodes + br + br

        output += "Total block count:" + 6 * tab + self.total_blocks + br
        output += "Total free block count:" + 5 * tab + self.total_free_blocks + br

        return output

    @staticmethod
    def getCreatorOSName(creator_os):
        os_name = "Not specified"

        if creator_os == 0:
            os_name = "Linux"
        elif creator_os == 1:
            os_name = "GNU Hurd"
        elif creator_os == 2:
            os_name = "Masix"
        elif creator_os == 3:
            os_name = "FreeBSD"
        elif creator_os == 4:
            os_name = "Lites"

        return os_name
