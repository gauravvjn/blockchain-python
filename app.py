from uuid import uuid4

from flask import Flask, request, jsonify

from blockchain import BlockChain


app = Flask(__name__)

blockchain = BlockChain()

node_address = uuid4().hex  # Unique address for current node


@app.route('/api/transactions', methods=['POST'])
def new_transaction():
    transaction_data = request.get_json()

    index = blockchain.create_new_transaction(**transaction_data)

    response = {
        'message': 'Transaction has been submitted successfully',
        'block_index': index
    }

    return jsonify(response), 201


@app.route('/api/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block(node_address)

    response = {
        'message': 'Successfully Mined the new Block',
        'block_data': block
    }
    return jsonify(response)


@app.route('/api/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': [vars(block) for block in blockchain.chain]
    }
    return jsonify(response), 200


@app.route('/api/nodes/register', methods=['POST'])
def register_nodes():
    return 'TODO'


@app.route('/api/nodes/resolve', methods=['GET'])
def consensus():
    return 'TODO'


app.run()
