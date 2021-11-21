import socket
import pickle
import os
from Receipt import Receipt
from Receipt import Unit
import re


HEADERSIZE = 20

s = None

def AddReceipt(receipt):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1244))
    msg = pickle.dumps(receipts)
    command = "addrecp"
    msg = bytes(f'{len(msg):<{HEADERSIZE-10}}{command}',"utf-8")+msg
    clientsocket.send(msg)
    ReceiveAnswer()


def GetReceipts():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1244))

    text = ""
    command = f'{"getrecps":<{HEADERSIZE-10}}'
    length = f'{len(text):<{HEADERSIZE-10}}'
    text = f"{length}{command}{text}"
    s.send(bytes(text,"utf-8"))
    ReceiveAnswer(s)
    
def ReceiveAnswer(s):
    print("Receiving")
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(20)
        if new_msg:
            if(msg is None):
                break;
            print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE-10])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))


        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print((full_msg[:HEADERSIZE]).decode("utf-8"))
            #print(full_msg[COMMANDSIZE:].decode("utf-8"))
            new_msg = True
            d = pickle.loads(full_msg[HEADERSIZE:])
            for r in d:
                print(r.ToString())
            full_msg = b''
            text = "end"
            text = f"{len(text):<{HEADERSIZE-10}}command"+text
            s.send(bytes(text,"utf-8"))
            break;


def Menu():
    sentinel  = True
    while(sentinel):
        inputCorrect = False
        num = -1
        while not inputCorrect: 
            inp = input("Wähle nächste Aktion:\n(1) Alle Rezepte anzeigen\n(2) Neues Rezept Hinzufügen\n")
            list_of_nums = re.findall('\d+', inp)
            if(len(list_of_nums) != 1):
                print("Nur eine Zahl darf eingegeben werden!")
            elif(int(list_of_nums[0])>2 or int(list_of_nums[0])<1):
                print("Nur 1 oder 2 sind möglich")
            else:
                num = int(list_of_nums[0])
                inputCorrect = True
        if(num == 1):
            GetReceipts()
        if(num == 2):
            AddReceipt()
        

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

clearConsole()
Menu()