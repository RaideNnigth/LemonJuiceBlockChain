# Path: wallet/juiceWallet.py
# Wallet class for JuiceCoin

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

import requests
import binascii

# JuiceWallet class
# This class represents a wallet with a public key, private key and address
# The amount is saved in the blockchain
# The address is the hash of the public key (publicKey->sha256->ripemd160 = address)
class JuiceWallet:
    def __init__(self, public_key_hex: str, private_key: RSA.RsaKey, address: str):
        self.lemonade_address = address                  # address is the hash of the public key
        self.public_key = public_key_hex                     # public key
        self.__private_key = private_key                  # private key
    
    # Print the wallet (Only for testing purposes)   
    def print_wallet(self):
        print("Wallet address:", self.lemonade_address)
        print("Wallet public key:", self.public_key)
        print("Wallet private key:", binascii.hexlify(self.__private_key.export_key()))
    
    # Sign the data with the private key
    def sign(self, data: bytes) -> bytes:
        # Create a SHA-256 hash of the data
        data_hash = SHA256.new(data)
        # Sign the hash using the private key
        signature = pkcs1_15.new(self.__private_key).sign(data_hash)
        return signature
