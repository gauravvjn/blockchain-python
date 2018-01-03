from blockchain import BlockChain


blockchain = BlockChain()


def print_blockchain(chain):
    for block in chain:
        print(block)


def main():
    print("Length of Current blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)

    blockchain.mine_block('address_x')
    print("\nAfter Mining . . . ")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)

    blockchain.mine_block('address_y')
    print("\nAfter One more Mining . . . ")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)

if __name__ == "__main__":
    main()
