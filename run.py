"""
mini-chain is a project to implement a blockchain in its most basic form.

run.py launches a flask REST api that wraps this peer node.
"""

from utils import Chain, Block
from errors import HashMismatchError, IndexMismatchError
from flask import Flask, request, jsonify

CHAIN = Chain()

PEERS = []

APP = Flask(__name__)

@APP.route("/chain")
def get_chain():
    """ get the full chain """
    return CHAIN.to_json()

@APP.route("/chain/add", methods=["POST"])
def add_block():
    """ add a new block to the chain """
    body = request.get_json()
    try:
        block = Block(len(CHAIN), body["data"], CHAIN.head().hash)
        CHAIN.add_block(block)
    except HashMismatchError:
        return "new block has incorrect previous hash", 200
    except IndexMismatchError:
        return "new block has incorrect index", 200
    except KeyError:
        return "expected data attribute in post body", 200

    return "added block at index {}".format(len(CHAIN) - 1)

@APP.route("/peers/add", methods=["POST"])
def add_peer():
    """ add a new peer to the network """
    pass

@APP.route("/block/<int:index>")
def get_block(index):
    """ get a block with a given index """
    try:
        block = CHAIN[index]
        return jsonify(block.to_json())
    except IndexError:
        return "the requested block does not exist", 404

APP.run(host="0.0.0.0", debug=True, port=8000)
