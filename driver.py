from blockchain import BlockChain


blockchain = BlockChain()


def mine_new_block():

    last_block = blockchain.get_last_block
    last_proof = last_block.proof
    proof = blockchain.create_proof_of_work(last_proof)

    # Sender "0" means that this node has mined a new block
    # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
    blockchain.create_new_transaction(
        sender="0",
        recipient="addressX",
        amount=1,
    )

    last_hash = last_block.get_block_hash
    block = blockchain.create_new_block(proof, last_hash)

    return {
        'index': block.index,
        'transaction': block.transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash,
    }


def print_blockchain(chain):
    for block in chain:
        print(block)


def main():
    print("Length of Current blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)
    mine_new_block()
    print("\nAfter Mining . . . ")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)
    mine_new_block()
    print("\nOne more Mining . . . ")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)

if __name__ == "__main__":
    main()
