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
    timestamp = 0

    def __init__(self, data):
        self.data = data
        if data == "Genesis":
            self.timestamp = 0
            self.previous_hash = 0
            self.nonce = 0
            self.height = 0
            self.difficulty = 0
        else:
            self.timestamp = datetime.datetime.now().timestamp()


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
        return "Block Hash: " + str(self.hash()) + "\nHeight: " + str(self.height) + "\nP block: " + str(self.previous_hash) + "\nBlock Data: " + str(self.data) + "\nNonce: " + str(self.nonce) + "\nDiff: " + str(self.difficulty) + "\nTimestamp: " + str(self.timestamp) + "\n--------------"

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Blockchain(metaclass=SingletonMeta):

    def __init__(self):
        self.chain= []
        self.block = Block("Genesis")
        self.chain.append(self.block)

    diff = 10
    maxNonce = 2**32

    def add(self, block):
        self.chain.append(block)

    def lastBlock(self):
        return self.chain[-1]


    def mine(self, block):
        target = 2 ** (256-self.diff)
        block.previous_hash = self.chain[-1].hash()
        block.height = len(self.chain)
        block.difficulty = self.diff
        for i in range(self.maxNonce):
            if int(block.hash(), 16) <= target:
                self.add(block)
                break
            else:
                block.nonce = format(random.getrandbits(32), "x")
                #block.nonce += 1
                #print(block.nonce)

    def checkDiff(self,block):
        target = 2 ** (256 - block.difficulty)
        if int(block.hash(), 16) <= target or block.data == "Genesis":
            return True
        else:
            return False

    def findBlock(self, hash):
        for item in self.chain:
            if hash == item.hash():
                return item
            else:
                break 
    
    def checkChain(self):
        for i in range(len(self.chain)):
            if i == 0:
                pass
            else:
                if self.chain[i].previous_hash != self.chain[i-1].hash():
                    return False
        return True
            




#blockchain = Blockchain()

#for n in range(1):
#    blockchain.mine(Block("Block " + str(n+1)))

#for block in blockchain.chain:
#    print(block)



