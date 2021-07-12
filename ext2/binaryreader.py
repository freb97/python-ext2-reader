import struct


class BinaryReader(object):
    """
    A binary reader for converting multiple values from a bytearray with error checks.

    Attributes
    ----------
    binary_data : bytes
        The byte array to extract values from.
    error : bool
        The error state of the reader.
    """

    def __init__(self, data):
        """
        Class constructor.

        Parameters
        ----------
        data : bytes
            The byte array to extract values from.
        """

        self.binary_data = data
        self.error = False

    def get_data_from_binary(self, start_position, end_position, byte_format):
        """
        Gets a value from the given binary data file and excepts read errors.

        Parameters
        ----------
        start_position : int
            The first index bit of the value.
        end_position : int
            The last index bit of the value.
        byte_format : str
            The format of the value (<H = 16bit Little-Endian Integer, <L = 32bit Little-Endian Integer, etc...)

        Returns
        -------
        int
            The integer representation of the selected bits.
        """

        if self.error:
            return 0

        raw_data = self.binary_data[start_position:end_position]

        try:
            data = struct.unpack(byte_format, raw_data)[0]

            return data
        except struct.error:
            self.error = True
            return 0
