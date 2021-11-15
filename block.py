import datetime
import hashlib
import random

class Block:
    height = 0
    data = None
    hash = None
    nonce = format(random.getrandbits(32), "x")
    difficulty = 0
    previous_hash = None
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.nonce).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.timestamp).encode('utf-8') +
        str(self.height).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nHeight: " + str(self.height) + "\nP block: " + str(self.previous_hash) + "\nBlock Data: " + str(self.data) + "\nNonce: " + str(self.nonce) + "\nDiff: " + str(self.difficulty) + "\n--------------"

class Blockchain:

    def __init__(self):
        self.chain= []
        self.block = Block("Genesis")
        self.chain.append(self.block)

    diff = 20
    maxNonce = 2**32

    def add(self, block):

        block.previous_hash = self.chain[-1].hash()
        block.height = len(self.chain)
        block.difficulty = self.diff

        self.chain.append(block)


    def mine(self, block):
        target = 2 ** (256-self.diff)
        for i in range(self.maxNonce):
            if int(block.hash(), 16) <= target:
                self.add(block)
                break
            else:
                block.nonce = format(random.getrandbits(32), "x")
                #block.nonce += 1
                #print(block.nonce)



#blockchain = Blockchain()

#for n in range(1):
#    blockchain.mine(Block("Block " + str(n+1)))

#for block in blockchain.chain:
#    print(block)



