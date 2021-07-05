class Stats(object):
    def __init__(self, file):
        self.file_name = file.file_name

        self.block_size = file.super_block.s_block_size
        self.blocks_per_group = file.super_block.s_blocks_per_group / self.block_size

        self.magic_number = hex(file.super_block.s_magic)
        self.creator_os = self.get_creator_os_name(file.super_block.s_creator_os)

    def to_string(self):
        br = "\n"
        tab = "\t"

        output = "EXT2 File statistics for file \"" + self.file_name + "\":" + br + br

        output += "Block size:" + 8 * tab + str(self.block_size) + " bytes" + br
        output += "Blocks per group:" + 6 * tab + str(int(self.blocks_per_group)) + br + br

        output += "Magic number (must equal 0xef53):" + 2 * tab + str(self.magic_number) + br
        output += "Created on OS:" + 7 * tab + self.creator_os + br

        return output

    @staticmethod
    def get_creator_os_name(creator_os):
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
