import datetime
import hashlib
import random
import jsonpickle

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
        #return "Block Hash: " + str(self.hash()) + "\nHeight: " + str(self.height) + "\nP block: " + str(self.previous_hash) + "\nBlock Data: " + str(self.data) + "\nNonce: " + str(self.nonce) + "\nDiff: " + str(self.difficulty) + "\nTimestamp: " + str(self.timestamp) + "\n--------------"
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

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
        try:
            with open('blockchain.pkl', 'rb') as inp:
                self.chain = jsonpickle.load(inp)
        except FileNotFoundError:
            with open('blockchain.pkl', 'wb') as outp:
                self.chain = []
                block = Block("Genesis")
                self.chain.append(block)
                jsonpickle.dump(self.chain, outp, jsonpickle.HIGHEST_PROTOCOL)

        if self.chain == None:
            self.chain = []
            block = Block("Genesis")
            self.chain.append(block)

    diff = 10
    maxNonce = 2**32

    def add(self, block):
        block.previous_hash = self.chain[-1].hash()
        block.height = len(self.chain)
        block.difficulty = self.diff
        self.chain.append(block)
        with open('blockchain.pkl', 'wb') as outp:
            jsonpickle.dump(self.chain, outp, jsonpickle.HIGHEST_PROTOCOL)


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


blockchain = Blockchain()

print(blockchain.chain)

#for n in range(1):
#    blockchain.mine(Block("Block " + str(n+1)))


##del blockchain


#for block in blockchain.chain:
#    print(block)

