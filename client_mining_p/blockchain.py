import hashlib
import json
from time import time
from uuid import uuid4
import os

from flask import Flask, jsonify, request

os.system( 'clear' )


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {

            'index' : len( self.chain ) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash( self.chain[ -1 ] ),

        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append( block )
        # Return the new block
        return block

    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps( block , sort_keys = True )
        block_string = string_object.encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256( block_string )
        hex_hash = raw_hash.hexdigest()


        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format

        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256( guess ).hexdigest()
        # return True or False
        if guess_hash[:6] == '000000':
            print( 'Guesh_hash:' , guess_hash )
        return guess_hash[:6] == '000000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():

    data = request.get_json()

    proof = data['proof']
    string_object = json.dumps( blockchain.last_block , sort_keys = True )
    block_string = string_object.encode()

    if blockchain.valid_proof( block_string , proof ):

        print( f'Miner submitted valid proof: { proof }' )

        block = blockchain.new_block( proof , blockchain.last_block )

        response = {

            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }

        return jsonify( response ), 200
    
    else:

        response = {

            'message': "Fail"
        }

        return jsonify( response ) , 200


@app.route('/chain', methods=['GET'])

def full_chain():

    response = {

        'length': len( blockchain.chain ),
        'chain': blockchain.chain,

    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():

    response = {
        'block' : blockchain.chain[ len( blockchain.chain ) - 1 ]
    }

    return jsonify(response), 200

@app.route('/', methods=['GET'])
def home():
    return "Sanity Check! 🤖", 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
