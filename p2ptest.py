from p2pnetwork.node import Node

from newblock import Block
from newblock import Blockchain

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
            if data['previous_hash'] == self.blockchain.lastBlock().hashOfBlock:
                block = Block(data['data'])
                block.items(data['height'],data['timestamp'],data['nonce'],data['previous_hash'],data['difficulty'],data['hashOfBlock'])
                self.blockchain.add(block)
                if self.blockchain.checkChain() and self.blockchain.checkDiff(block):
                    print("Novy block bol overeny a pridany")
                    msg = self.blockchain.lastBlock().__dict__
                    msg['msg'] = "New block"
                    noNodes = [node]
                    self.send_to_nodes(msg,noNodes)
                else:
                    print("Block nebol overeny a nebol pridany")
                    self.blockchain.removeLast()
            else:
                msg = {
                    "height": self.blockchain.chain[-1].height,
                    "msg": "Get Height",
                }
                self.send_to_node(node,msg)
        elif data['msg'] == "Sync block":
            if data['hashOfBlock'] != self.blockchain.lastBlock().hashOfBlock:
                block = Block(data['data'])
                block.items(data['height'],data['timestamp'],data['nonce'],data['previous_hash'],data['difficulty'],data['hashOfBlock'])
                self.blockchain.add(block)
                if self.blockchain.checkChain() and self.blockchain.checkDiff(block):
                    print("Block bol overeny a pridany")
                else:
                    print("Block nebol overeny a nebol pridany")
                    self.blockchain.removeLast()
            else:
                pass
        elif data['msg'] == "Get Height":
            if data['height'] > self.blockchain.lastBlock().height:
                chyba = data['height'] - self.blockchain.lastBlock().height
                print("chyba mi " + str(chyba))
                for i in range(1, chyba+1, 1):
                    msg = {
                        "height": self.blockchain.lastBlock().height,
                        "msg": "Get Block",
                        "block_height": self.blockchain.lastBlock().height + i
                    }
                    self.send_to_node(node,msg)
            else:
                print("nechyba mi ziadny blok ")
        elif data['msg'] == "Get Block":
            msg = self.blockchain.chain[data['block_height']].__dict__
            msg['msg'] = "Sync block"
            self.send_to_node(node,msg)

        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: (" + self.id + "): " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop (" + self.id + "): ")