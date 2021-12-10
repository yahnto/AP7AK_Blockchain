import newblock as block
from newblock import Block
from p2ptest import MyOwnPeer2PeerNode
import os

menu_options = {
    1: 'Add Hacked Block',
    2: 'Adjust difficulty',
    3: 'Show blockchain',
    4: 'Exit',
}
def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key])

if __name__=='__main__':
    blockchain = block.Blockchain()
    print("chain",blockchain.checkChain())
    if blockchain.checkChain() == False:
        print("Corrupted chain")
        blockchain.chain.clear()
        block = Block("Genesis")
        blockchain.chain.append(block)
        os.remove("data.json")
    node = MyOwnPeer2PeerNode("127.0.0.1", 8001, 2)
    node.connect_with_node('127.0.0.1', 8002)
    node.start()
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            data = input("Type data:")
            blockchain.mine(Block(data))
            msg = blockchain.chain[-1].__dict__
            msg['msg'] = "New block"
            msg['previous_hash'] = "haha hacked"
            blockchain.removeLast()
            node.send_to_nodes(msg)
        elif option == 2:
            #diff = input("Type diffuiculty:")
            #blockchain.diff = int(diff)
            blockchain.chainLen()
        elif option == 3:
            for b in blockchain.chain:
                print(b)
        elif option == 4:
            node.stop()
            exit()