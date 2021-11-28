import json
import jsonpickle

class Block:
    def __init__(self,data):
        self.data = data
        self.timestamp = 0
        self.previous_hash = 0
        self.nonce = 0
        self.height = 0
        self.difficulty = None

class Blockchain:
    def __init__(self):
        self.chain = []
    
    def add(self,block):
        self.chain.append(Block(block))



blockchain = Blockchain()
blockchain.add("halo ts me")
blockchain.add("halo ts me 1 ")
blockchain.add("halo ts me 2")
block = Block("karol")
test = jsonpickle.encode(blockchain.chain)

with open('data.json', 'w') as f:
    f.write(test)

with open('data.json', 'r') as f:
    untest = jsonpickle.decode(f.read())


#print(test)
print(untest[1].__dict__)