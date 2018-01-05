import requests

from blockchain import BlockChain


blockchain = BlockChain()


# --------------------------- Testing The Blockchain Class ---------------------------------------------


def print_blockchain(chain):
    for block in chain:
        print(vars(block))


def class_tests():
    print("Length of Current blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)

    blockchain.mine_block('address_x')
    print("\nAfter Mining . . .")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)

    blockchain.mine_block('address_y')
    print("\nAfter One more Mining . . .")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)


# --------------------------------- Testing Blockchain APIs --------------------------------------------


def register_node(node_addr, parent_server):
    resp = requests.post(parent_server + '/register-node', json={'address': node_addr})
    print("\nOn Server {}: Node-{} has been registered successfully!\n".format(parent_server, node_addr))
    return resp


def create_transaction(server, data):
    resp = requests.post(server + '/create-transaction', json=data).json()
    print("On Server {}: Transaction has been processed!\n".format(server))
    return resp


def mine_block(server):
    resp = requests.get(server + '/mine').json()
    print("On Server {}: Block has been mined successfully!\n".format(server))
    return resp


def get_server_chain(server):
    resp = requests.get(server + '/chain').json()
    print("On Server {}: Chain is-\n{}\n".format(server, resp))
    return resp


def sync_chain(server):
    print("On Server {}: Started Syncing Chain . . .".format(server))
    resp = requests.get(server + '/sync-chain')
    print("On Server {}: Chain synced!\n".format(server))
    return resp


def api_tests():

    server1 = 'http://127.0.0.1:5000'
    server2 = 'http://127.0.0.1:5001'

    register_node(server2, server1)  # server2 node will be register inside server1

    create_transaction(server2, {'sender': 'I', 'recipient': 'you', 'amount': 3})

    mine_block(server2)  # Mined a new block on server2

    get_server_chain(server1)  # server1's chain
    get_server_chain(server2)  # server2's chain

    sync_chain(server1)  # updating server1's chain with neighbour node's chain

    get_server_chain(server1)  # server1's chain after syncing


if __name__ == "__main__":
    class_tests()
    api_tests()
