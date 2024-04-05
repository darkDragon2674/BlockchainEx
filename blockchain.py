import hashlib
import datetime
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

class Block:
    blockno = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0 #this is 0x0 due to hex encryption
    timestamp = datetime.datetime.now()
    transaction = {}
    n = 0
    
    
    def __init__(self, data):
        self.data = data
    
    def hash(self):#the hashing process
        self.n = self.n + 1
        h = hashlib.sha256()
        h.update(
                str(self.nonce).encode('utf-8') + 
                str(self.data).encode('utf-8') + 
                str(self.nonce).encode('utf-8') +
                str(self.timestamp).encode('utf-8') +
                str(self.previous_hash).encode('utf-8') + 
                str(self.blockno).encode('utf-8'))
        return h.hexdigest()

    
    def __str__(self):
        return("_______________" + 
              "\nBlockNo: " + str(self.blockno) + 
              "\nHash: " + str(self.hash()) + 
              "\nData: " + str(self.data) + 
              "\nTime: " + str(self.timestamp) +
              "\nHashes: " + str(self.nonce) + 
              "\n_______________")
        
        
class Blockchain:

    diff = 17 
    li = [diff, diff + 1, diff + 2]
    maxNonce = 2**32
    target = 2 ** (260 -diff) #thus, higher the difficulity, less is the range of the required hashes in which you need to find a target, thus it takes more iterations to find a nonce
    head = block = Block("Genesis")

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockno = self.block.blockno + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                #decides if block is to be added based on the validity of the hash, like if the nonce assigned is less than the target value
                self.add(block)
                
                f = open("BLOCKCHAIN.txt", "a")
                f.writelines(str(block))
                f.close() 
                break
            else:
                block.nonce += 1
                

blockchain = Blockchain()
n = 0
open('BLOCKCHAIN.txt', 'w').close()

# TKINTER INITIALIZING
main = tk.Tk()
main.title("BLOCKCHAIN HOME")
main.configure(bg = "gold")


sel = tk.StringVar()

#Scrollbar, needs fixing
scrollbar = tk.Scrollbar()
scrollbar.pack(side = "right", fill= "y")




#Functions for mining and displaying in tkinter
def select_1():
    sel.set("Transaction complete --------- 1 more block added")
    blockchain.mine(Block("Block: " + str(n + 1) ))

def select_2():
    str_ = ""
    f = open("BLOCKCHAIN.txt", "r")
    a = f.readlines() 
    for i in a:
        str_ = str_ + i
    sel.set(str_)
    f.close()
    
    
    
    
#Starting lables and text    
l1 = tk.Label(main, text = """Hello there, and welcome to the Blockchain program
         By - Arnavdeep Singh Arneja""", bg = "gold")
l2 = tk.Label(main, text = """Blockchain is a continuously growing list of transactions, or blocks, which are linked and secured using encrypted 'hashes'
      
      Mining is the process of making new blocks on the preexisting genesis block""", bg = "gold")
l1.pack()
l2.pack()

#Setting of textvariables
v = tk.IntVar() 

#Buttons for the mining and displaying
r1 = tk.Radiobutton(main, text='Mine', variable=v, value=1, command = select_1, bg = "gold")
r2 = tk.Radiobutton(main, text='Display', variable=v, value=2, command = select_2, bg = "gold")
r1.pack(anchor = "w")
r2.pack(anchor = "w")

l3 = tk.Label(main, textvariable = sel, bg = "gold")
l3.pack()


main.mainloop() 
