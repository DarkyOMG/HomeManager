
import socket
import time
import pickle

from Receipt import Receipt
from Receipt import Unit

currentReceipts = []
HEADERSIZE = 20

def AddReceipt(receipt=None,name=None,ingridients=None):
    if receipt is not None:
        currentReceipts.append(receipt)
    else:
        temp = Receipt(name,ingridients)
        currentReceipts.append(Receipt)
def RemoveReceipt(receipt):
    currentReceipts.remove(receipt)
def RemoveReceiptByName(name):
    for r in currentReceipts:
        if(r.name == name):
            currentReceipts.remove(r)



def main():
        #!/usr/bin/env python3
    #Testreceipts
    AddReceipt(Receipt("Nudeln mit Pesto",[("Nudeln",500, Unit.Gramm),("Pesto",200,Unit.Milliliter)]))
    AddReceipt(Receipt("Gnocchi mit Spinat",[("Gnocchi",500,Unit.Gramm),("Spinat",300,Unit.Gramm),("Sojasahne",125,Unit.Milliliter)]))
    AddReceipt(Receipt("Linsenlasagne",[("Lasagneplatten",500,Unit.Gramm),("Zucchini",300,Unit.Gramm),("Tomate",2,Unit.Stueck)]))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1244))
    s.listen(5)

    while True:
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")

        full_msg = ''
        new_msg = True
        while True:
            msg = clientsocket.recv(20)
            if(msg is None):
                break;
            if new_msg:
                print("new msg len:",msg[:HEADERSIZE-10])
                msglen = int(msg[:HEADERSIZE-10])
                command = msg[HEADERSIZE-10:HEADERSIZE]
                print(command.strip())
                new_msg = False

            print(f"full message length: {msglen}")

            full_msg += msg.decode("utf-8")

            print(len(full_msg))
            print(HEADERSIZE)
            print(msglen)

            lastmessage = ""
            if len(full_msg)-HEADERSIZE == msglen:
                print("full msg recvd")
                print(full_msg[HEADERSIZE:])
                lastmessage = full_msg[HEADERSIZE:]
                new_msg = True
                full_msg = ""
                if(ExecuteCommand(clientsocket,command,lastmessage)):
                    break;

def ExecuteCommand(s, command, message):
    print(command)
    if(command == "test"):
        msg = "Thank youuuu for " + lastmessage
        msg = f"{len(msg):<{HEADERSIZE-10}}command"+msg
        s.send(bytes(msg,"utf-8"))
    if(command == "getrecps"):
        msg = pickle.dumps(currentReceipts)
        length = f'{len(msg):<{HEADERSIZE-10}}'
        command = f'{"recpsans":<{HEADERSIZE-10}}'
        msg = f"{length}{command}{msg}"
        s.send(msg)
    if(command == "addrecps"):
        print("new Receipt")
    if(command == "end"):
        s.close()
        return True
    return False

if __name__ == "__main__":
    main()
