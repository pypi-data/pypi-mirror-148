import string, random, sys, os
from sys import intern

class Encrypt:
            def __init__(self):
                self.get = {
                'upper': string.ascii_uppercase,
                'lower': string.ascii_lowercase ,
                'letther': string.ascii_letters ,
                'digits': string.digits,
                'speciall': string.punctuation
                }
                self.data = ''
                self.hex_logic = 0xaa, None
            def Generate_String(self, size):
                chars = self.get['letther']+str(self.get['digits'])+self.get['speciall']
                return ''.join(random.choice(chars) for _ in range(size))

            def ciphertext(self, options='encrypt', text="test"):
                mapkey = {'A': '9', 'B': 'O', 'C': '3', 'D': 'R', 'E': 'v', 'F': "'", 'G': ';', 'H': '(', 'I': '2', 'J': ',', 'K': 'm', 'L': 'w', 'M': 'g', 'N': '[', 'O': '"', 'P': '}', 'Q': 'q', 'R': '7', 'S': 'T', 'T': '1', 'U': 'K', 'V': ']', 'W': 'Y', 'X': 'b', 'Y': 'e', 'Z': 'l', 'a': 'u', 'b': 'H', 'c': 'V', 'd': '6', 'e': ':', 'f': '5', 'g': 'B', 'h': 'y', 'i': ' ', 'j': 'z', 'k': 'N', 'l': '<', 'm': 'F', 'n': '!', 'o': '0', 'p': '^', 'q': 'p', 'r': 'I', 's': '\\', 't': 'j', 'u': 'd', 'v': 'c', 'w': 'W', 'x': '>', 'y': 'Q', 'z': '/', '0': '~', '1': 'C', '2': '&', '3': '.', '4': '`', '5': '@', '6': 'D', '7': '$', '8': '=', '9': 'o', ':': 'E', '.': 'L', ';': '{', ',': '#', '?': 'S', '!': 's', '@': 't', '#': 'J', '$': '_', '%': '+', '&': 'k', '(': 'i', ')': '?', '+': 'a', '=': 'U', '-': '*', '*': '-', '/': 'M', '_': '%', '<': 'X', '>': 'A', ' ': 'G', '[': 'n', ']': 'f', '{': 'h', '}': 'x', '`': 'r', '~': 'Z', '^': 'P', '"': '8', "'": '4', '\\': ')'} , self.hex_logic
                self.chars = self.get['letther']+str(self.get['digits'])+self.get['speciall']
                public_key = ''
                private_key = ''
                def generate_key(self):
                   """Generate an key for our cipher"""
                   global mapkey
                   shuffled = sorted(self.chars, key=lambda k: random.random())
                   mapkey = dict(zip(self.chars, shuffled)), self.hex_logic
                   return mapkey
                def login_(self, mapx=2):
                    exract_key= int(mapkey[1:][0][:1][0])
                    if exract_key%mapx == 0:
                        private_key = exract_key is self.hex_logic[0]
                        public_key = mapkey[:1][0]
                        return private_key, public_key
                    return False, None
                    ########Encrypt text using chipherset 128bit
                def encrypt(key, plaintext):
                    """Encrypt the string and return the ciphertext"""
                    return ''.join(key[l] for l in plaintext)
                def decrypt(key, ciphertext):
                    """Decrypt the string and return the plaintext"""
                    flipped = {v: k for k, v in key.items()}
                    return ''.join(flipped[l] for l in ciphertext) 

                log = login_(self)
                pent0 = []
                pent1 = []
                if log[0] == True:
                    for data in log[1]:
                                pent0.append(data)
                                pent1.append(log[1][data])
                    key = dict(zip(pent0, pent1))

                if options == 'encrypt':
                    try:
                        return encrypt(key, text)
                    except:
                        return None
                elif options == 'decrypt':
                    try:
                        return decrypt(key, text)
                    except:
                        return None
                elif options == 'generate-key':
                    mapkey = generate_key(self)
                    return mapkey
                elif options == 'show-key':
                    try:
                        return key
                    except:
                        return None
                else:
                    return None

            def HexaDecimall(self, options='encrypt'):
                def Hex_to_Str(self):
                    hex = self.data.replace('-0x128', '')
                    if 0xaa in self.hex_logic and self.data[:2] == '0x':
                        hex = self.data[2:]
                    output = bytes.fromhex(hex).decode('utf-8')
                    return self.ciphertext(text=output, options='decrypt')

                def Str_to_hex(self):
                    if 0xaa in self.hex_logic:
                        self.data = self.ciphertext(text=self.data, options='encrypt')
                        output = f"{self.data}".encode('utf-8')
                        return str(output.hex()+'-0x128')
                    return None
                if options.lower()=='decrypt':
                    data = Hex_to_Str(self)
                    return data
                elif options.lower()=='encrypt':
                    data = Str_to_hex(self)
                    return data
                else:
                    return 