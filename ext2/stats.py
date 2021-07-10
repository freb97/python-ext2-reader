from ext2 import file


class Stats(object):
    """
    File statistics representation.

    Attributes
    ----------
    file : bytearray
        The file to retrieve statistics from.
    output : str
        The file statistics output as a string.

    Methods
    -------
    to_string
        Gets the file statistics as a string.
    formatted_line
        Creates a formatted line for file statistics representation.
    get_creator_os_name
        Gets the file creator os name from the integer input.
    """

    def __init__(self, input_file):
        """
        Class constructor.

        Parameters
        ----------
        input_file : file.File
            The file to retrieve statistics from.
        """

        self.file = input_file
        self.output = ""
        
    def get_statistics(self):
        """
        Gets the file statistics.

        Returns
        -------
        str
            The file statistics as a string.
        """

        if self.output != "":
            return self.output

        file_name = self.file.file_name

        block_size = self.file.super_block.s_block_size
        blocks_per_group = self.file.super_block.s_blocks_per_group / block_size
        block_group_count = len(self.file.block_groups)
        free_blocks = self.file.group_descriptor.bg_free_blocks_count
    
        magic_number = hex(self.file.super_block.s_magic)
        creator_os = self.get_creator_os_name(self.file.super_block.s_creator_os)
    
        inode_size = self.file.super_block.s_inode_size
        free_inodes = self.file.group_descriptor.bg_free_inodes_count

        self.formatted_line("EXT2 File statistics for file", file_name, "\n", tab_size=3)

        self.formatted_line("Magic number (must equal 0xef53)", str(magic_number), tab_size=2)
        self.formatted_line("Created on OS", creator_os, tab_size=7)
        self.formatted_line()

        self.formatted_line("Block size", str(block_size), "bytes", tab_size=8)
        self.formatted_line("Blocks per group", str(int(blocks_per_group)), tab_size=6)
        self.formatted_line("Block group count", str(int(block_group_count)), tab_size=6)
        self.formatted_line("Free blocks count", str(int(free_blocks)), tab_size=6)
        self.formatted_line()

        self.formatted_line("Inode size", str(int(inode_size)), tab_size=8)
        self.formatted_line("Free inode count", str(int(free_inodes)), tab_size=6)

        return self.output

    def formatted_line(self, prefix="", content="", suffix="", tab_size=0):
        """
        Creates a formatted line for file statistics representation.

        Parameters
        ----------
        prefix : str
            The prefix of the line.
        content : str
            The actual value content.
        suffix : str
            The suffix of the line.
        tab_size : int
            The amount of tabs to add between the prefix and the content.

        Returns
        -------
        str
            The formatted line of statistics information.
        """

        if prefix != "":
            prefix += ":"

        if suffix != "":
            suffix = " " + suffix

        self.output += prefix + tab_size * "\t" + content + suffix + "\n"

    @staticmethod
    def get_creator_os_name(creator_os):
        """
        Gets the file creator os name from the integer input.

        Parameters
        ----------
        creator_os : int
            The integer representation of the file creator os from the super block.

        Returns
        -------
        str
            The creator os name.
        """

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
