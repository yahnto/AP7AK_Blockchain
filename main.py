import block

menu_options = {
    1: 'Add Block',
    2: 'Adjust difficulty',
    3: 'Show blockchain',
    4: 'Exit',
}
def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key])

if __name__=='__main__':
    blockchain = block.Blockchain()
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            data = input("Type data:")
            blockchain.mine(block.Block(data))
        elif option == 2:
            diff = input("Type diffuiculty:")
            blockchain.diff = int(diff)
        elif option == 3:
            for b in blockchain.chain:
                print(b)
        elif option == 4:
            exit()