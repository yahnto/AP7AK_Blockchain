import datetime
import hashlib
import random
import jsonpickle

class Block:
    height = 0
    data = None
    hashOfBlock = None
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
            self.hashOfBlock = self.hash()
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
        return "Block Hash: " + str(self.hashOfBlock) + "\nHeight: " + str(self.height) + "\nP block: " + str(self.previous_hash) + "\nBlock Data: " + str(self.data) + "\nNonce: " + str(self.nonce) + "\nDiff: " + str(self.difficulty) + "\nTimestamp: " + str(self.timestamp) + "\n--------------"

    def items(self,height,timestamp,nonce,previous_hash,difficulty,hashOfBlock):
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.height = height
        self.difficulty = difficulty
        self.hashOfBlock = hashOfBlock

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Blockchain(metaclass=SingletonMeta):

    def __init__(self):
        try:
            with open('data.json', 'r') as f:
                self.chain = jsonpickle.decode(f.read())
        except FileNotFoundError:
            with open('data.json', 'w') as f:
                self.chain = []
                block = Block("Genesis")
                self.chain.append(block)
                f.write(jsonpickle.encode(self.chain))

    def lastBlock(self):
        return self.chain[-1]
    

    def add(self, block):
        self.chain.append(block)
        with open('data.json', 'w') as f:
            f.write(jsonpickle.encode(self.chain))

    def removeLast(self):
        self.chain.pop()
        with open('data.json', 'w') as f:
            f.write(jsonpickle.encode(self.chain))

    diff = 10
    maxNonce = 2**32

    def mine(self, block):
        target = 2 ** (256-self.diff)
        block.previous_hash = self.chain[-1].hash()
        block.height = len(self.chain)
        block.difficulty = self.diff
        for i in range(self.maxNonce):
            if int(block.hash(), 16) <= target:
                block.hashOfBlock = block.hash()
                self.add(block)
                break
            else:
                block.nonce = format(random.getrandbits(32), "x")
                #block.nonce += 1
                #print(block.nonce)

    def findBlock(self, hash):
        for item in self.chain:
            if hash == item.hash():
                return item
            else:
                break 
    
    def checkChain(self):
        if len(self.chain) != 1:
            for i in range(len(self.chain)):
                if i == 0:
                    pass
                else:
                    if (self.chain[i].previous_hash != self.chain[i-1].hash()) or (self.chain[i].hash() !=  self.chain[i].hashOfBlock):
                        return False
            return True
        return True
    
    def checkDiff(self,block):
        target = 2 ** (256 - block.difficulty)
        if int(block.hash(), 16) <= target or block.data == "Genesis":
            return True
        else:
            return False

    def lastBlock(self):
        return self.chain[-1]
            

blockchain = Blockchain()

