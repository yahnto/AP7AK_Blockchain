from p2pnetwork.node import Node

from block import Block
from block import Blockchain

class MyOwnPeer2PeerNode (Node):
    blockchain = Blockchain()
    # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(MyOwnPeer2PeerNode, self).__init__(host, port, id, callback, max_connections)
        print("MyPeer2PeerNode: Started")

    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        msg = {
            "height": self.blockchain.chain[-1].height,
            "msg": "Get Height",
        }
        self.send_to_node(node,msg)
        
    def inbound_node_connected(self, node):
        msg = {
            "height": self.blockchain.chain[-1].height,
            "msg": "Get Height",
        }
        self.send_to_node(node,msg)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: (" + self.id + "): " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: (" + self.id + "): " + node.id)

    def node_message(self, node, data):
        if data['msg'] == "New block":
            block = Block(data['data'])
            block.height = data['height']
            block.timestamp = data['timestamp']
            block.nonce = data['nonce']
            block.previous_hash = data['previous_hash']
            block.difficulty = data['difficulty']
            self.blockchain.chain.append(block)
            print("Block bol pridany")
        elif data['msg'] == "Get Height":
            if data['height'] > self.blockchain.chain[-1].height:
                chyba = data['height'] - self.blockchain.chain[-1].height
                print("chyba mi " + str(chyba))
                for i in range(1, chyba+1, 1):
                    msg = {
                        "height": self.blockchain.chain[-1].height,
                        "msg": "Get Block",
                        "block_height": self.blockchain.chain[-1].height + i
                    }
                    self.send_to_node(node,msg)
            else:
                print("nechyba mi ziadny blok ")
        elif data['msg'] == "Get Block":
            msg = self.blockchain.chain[data['block_height']].__dict__
            msg['msg'] = "New block"
            print(msg)
            self.send_to_node(node,msg)

        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")