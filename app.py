from uuid import uuid4

import requests
from flask import Flask, jsonify, url_for, request

from blockchain import BlockChain


app = Flask(__name__)

blockchain = BlockChain()

node_address = uuid4().hex  # Unique address for current node


@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    """
    Input Payload:
    {
        "sender": "address_1"
        "recipient": "address_2",
        "amount": 3
    }
    """
    transaction_data = request.get_json()

    index = blockchain.create_new_transaction(**transaction_data)

    response = {
        'message': 'Transaction has been submitted successfully',
        'block_index': index
    }

    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block(node_address)

    response = {
        'message': 'Successfully Mined the new Block',
        'block_data': block
    }
    return jsonify(response)


@app.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.get_serialized_chain
    }
    return jsonify(response)


@app.route('/register-node', methods=['POST'])
def register_node():

    node_data = request.get_json()

    blockchain.create_node(node_data.get('address'))

    response = {
        'message': 'New node has been added',
        'node_count': len(blockchain.nodes),
        'nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/sync-chain', methods=['GET'])
def consensus():

    def get_neighbour_chains():
        neighbour_chains = []
        for node_address in blockchain.nodes:
            resp = requests.get(node_address + url_for('get_full_chain')).json()
            chain = resp['chain']
            neighbour_chains.append(chain)
        return neighbour_chains

    neighbour_chains = get_neighbour_chains()
    if not neighbour_chains:
        return jsonify({'message': 'No neighbour chain is available'})

    longest_chain = max(neighbour_chains, key=len)  # Get the longest chain

    if len(blockchain.chain) >= len(longest_chain):  # If our chain is longest, then do nothing
        response = {
            'message': 'Chain is already up to date',
            'chain': blockchain.get_serialized_chain
        }
    else:  # If our chain isn't longest, then we store the longest chain
        blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
        response = {
            'message': 'Chain was replaced',
            'chain': blockchain.get_serialized_chain
        }

    return jsonify(response)


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=5000, type=int)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)
