class HashMismatchError(Exception):
    """ raised when a previous block hash is incorrect """
    pass

class IndexMismatchError(Exception):
    """ raised when a new block has an incorrect index """
    pass

class InvalidChainError(Exception):
    """ raised when an invalid chain is validation checked """
    pass
