class Block(object):
    def __init__(self):
        self.data = None

    def get(self, file_input, block_id, block_size):
        self.data = file_input[block_id*block_size:block_id*block_size+block_size]
