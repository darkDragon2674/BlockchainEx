import hashlib
import json
from time import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains 4 leading zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int> Previous Proof
        :return: <int> New Proof
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


def main():
    blockchain = Blockchain()

    while True:
        print("\nBlockchain Menu:")
        print("1. Mine a new block")
        print("2. Create a new transaction")
        print("3. Display the blockchain")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Mine a new block
            last_block = blockchain.last_block
            last_proof = last_block['proof']
            proof = blockchain.proof_of_work(last_proof)

            # Reward for mining
            blockchain.new_transaction(
                sender="0",
                recipient="me",
                amount=1,
            )

            # Forge the new Block by adding it to the chain
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)

            print("\nBlock mined successfully.")

        elif choice == "2":
            # Create a new transaction
            sender = input("Enter sender: ")
            recipient = input("Enter recipient: ")
            amount = float(input("Enter amount: "))
            index = blockchain.new_transaction(sender, recipient, amount)

            print(f"\nTransaction will be added to Block {index}")

        elif choice == "3":
            # Display the blockchain
            print("\nBlockchain:")
            for block in blockchain.chain:
                print(block)
            print("")

        elif choice == "4":
            # Exit
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
