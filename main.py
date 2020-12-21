import argparse
import json
import base64
import os
import string
import random

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join([chr(random.randint(32, 255)) for i in range(length)])
    return (result_str)


def encrypt(inp,passwddefin):
    orig = (inp)
    passwd = (passwddefin)
    if not len(orig) == len(passwd):
        quit("Incorrect key!")
    origshift = ""
    origascii = [ord(c) for c in orig[::-1]]
    passwdascii = [ord(c) for c in passwd[::-1]]
    res_list = []
    for i in range(0, len(origascii)):
        appendout = origascii[i] + passwdascii[i]
        a = appendout
        b = str(a - int(a))
        res_list.append(appendout)
    res_str = str(res_list).replace("[", "").replace("]", "").replace(",", "nC").replace(" ", "hl")
    out = res_str
    return(out)
def decrypt(inp, passwddefin):
    orig = (inp)
    passwd = (passwddefin)
    encrypted = orig
    key = passwd
    encrypted = (encrypted.replace("nC", " ").replace("hl", "")).split()
    key = [ord(c) for c in key[::-1]]
    out = ""
    for x in range(0, len(key)):
        calc = int(encrypted[x]) - int(key[x])
        out = out + chr(calc)
    out = out[::-1]
    return(out)

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", help="Action")
parser.add_argument("-f", "--file", help="Main file")
parser.add_argument("-k", "--key", nargs='?', default="", help="Key file")
args = parser.parse_args()
action=args.action
file=args.file
key=args.key
if action in ["lock", "enc", "encrypt"]:
    filename = os.path.basename(file)
    with open(file, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_out = base64_encoded_data.decode('utf-8')
    key = get_random_string(len(base64_out))
    keyfile = open((os.path.splitext(filename)[0] + ".key"), 'w+')
    keyfile.write(key)
    keyfile.close()
    encdata = encrypt(base64_out, key)
    filecont = {"fn": filename, "data": encdata}
    outfile = open(os.path.splitext(filename)[0] + ".locked", 'w+')
    json.dump(filecont, outfile)
    outfile.close()
elif action in ["key", "dec", "decrypt"]:
    file = input("encrypted file: ")
    key = open(input("Key: "), 'r').read()
    filecont = json.load(open(file, 'r'))
    filename = filecont["fn"]
    encrypted_data = filecont["data"]
    print(filename, "is being de-encrypted")
    b64 = decrypt(encrypted_data, key)
    base64_file_bytes = b64.encode('utf-8')
    with open(filename, 'wb') as file_to_save:
        decoded_file_data = base64.decodebytes(base64_file_bytes)
        file_to_save.write(decoded_file_data)
