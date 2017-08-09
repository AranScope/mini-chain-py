"""
basic implementation of a blockchain, no proof of work is included.
"""

import hashlib
from time import time
import json
from errors import HashMismatchError, IndexMismatchError, InvalidChainError

class Block(object):
    """
    Represents a block in the chain.
    """
    def __init__(self, index, data, previous_hash=None):
        self.index = index
        self.timestamp = time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        returns the sha256 hash of the block.
        the hash is computed from the index, timestamp, data and previous hash.
        """
        block_data = ''.join(map(str, [self.index, self.timestamp, self.data, self.previous_hash]))
        block_data_bytes = str.encode(block_data)
        block_hash = hashlib.sha256()
        block_hash.update(block_data_bytes)
        block_hash_hex = block_hash.hexdigest()

        return block_hash_hex

    def to_json(self):
        """
        Convert the block to JSON, used for sending over the network.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Chain(object):
    """
    Represents the chain itself.
    """
    genesis = Block(0, 'genesis')

    def __init__(self):
        self.blocks = [Chain.genesis]

    def __iter__(self):
        return iter(self.blocks)

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, key):
        return self.blocks[key]

    def is_empty(self):
        """ check if the chain is empty, i.e. in an invalid state as no genesis block exists """
        return len(self.blocks) == 0

    def head(self):
        """ get the most recently added block in the chain """
        return self.blocks[-1]

    @staticmethod
    def validate_next_block(block, next_block):
        """ check if the previous hash and index of the new block are valid """
        if next_block.previous_hash != block.hash:
            raise HashMismatchError("invalid previous block hash")
        if next_block.index != block.index + 1:
            raise IndexMismatchError("invalid next block index")

    def add_block(self, block):
        """ add a new block to the chain, return True if successful """
        try:
            self.validate_next_block(self.blocks[-1], block)
            self.blocks.append(block)
        except HashMismatchError as hash_error:
            raise InvalidChainError(str(hash_error))
        except IndexMismatchError as index_error:
            raise InvalidChainError(str(index_error))


    def validate(self):
        """ check if a given blockchain is valid """
        if self.is_empty():
            raise InvalidChainError("missing genesis block")
        elif self.blocks[0] != Chain.genesis:
            raise InvalidChainError("incorrect genesis block")
        else:
            for current_block, next_block in zip(self.blocks[0:], self.blocks[1:]):
                try:
                    self.validate_next_block(current_block, next_block)
                except HashMismatchError as hash_error:
                    raise InvalidChainError(str(hash_error))
                except IndexMismatchError as index_error:
                    raise InvalidChainError(str(index_error))

    def to_json(self):
        """ convert the chain to a json array """
        blocks = [block.to_json() for block in self.blocks]
        chain_json = json.dumps(blocks, indent=4)
        return chain_json
