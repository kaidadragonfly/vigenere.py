#!/usr/bin/env python

# An implementation of the vigenere cipher.
#
# Takes the key and plaintext as command line arguments.
# Only works on ASCII text.  Use Unicode at your own peril.
try:
    from functools import reduce
except:
    pass

from sys import argv
from getopt import getopt

low_code = ord(' ')
high_code = ord('~')
coderange = high_code - low_code + 1

def ascii_to_keyspace(s):
    return map(lambda c:ord(c) - low_code, s)

def keyspace_to_ascii(ords):
    return reduce(lambda x, y: x + y,map(lambda c:chr(c + low_code), ords))

def code_add(x,y):
    return (x + y) % coderange

def code_sub(x, y):
    return (y - x) % coderange

def pad(s, length):
    while len(s) < length:
        s += s
    return s[:length]

def viginere(key, text, code_func):
    key  = pad(key, max(len(key),len(text)))
    text = pad(text, max(len(key),len(text)))
    key_ords = ascii_to_keyspace(key)
    text_ords = ascii_to_keyspace(text)
    return keyspace_to_ascii(map(code_func, key_ords, text_ords))

def cipher(key, plaintext):
    return viginere(key, plaintext, code_add)

def decipher(ciphertext, key):
    return viginere(key, ciphertext, code_sub)

def usage():
    print("usage: ./viginere.py [-n length] key [key2, key3, ...] text")

# Main logic
if len(argv) < 3:
    usage()
    exit(-1)

args = argv[1:]
length = None
oplist, args = getopt(args,'n:')
for opt, arg in oplist:
    if opt in ('-n'):
        length = int(arg)

length = max(map(len,args)) if (length == None) else length


print("     " + length * '_')
print("enc: " + reduce(cipher, args)[:length])
print("dec: " + reduce(decipher, reversed(args))[:length])
