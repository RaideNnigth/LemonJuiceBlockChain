# Path: wallet/juiceWallet.py
# Wallet class for JuiceCoin

import binascii

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


# JuiceWallet class
# This class represents a wallet with a public key, private key and address
# The amount is saved in the blockchain
# The address is the hash of the public key (publicKey->sha256->ripemd160 = address)
class JuiceWallet:
    def __init__(self, public_key, private_key, address):
        self.lemonade_address = address                  # address is the hash of the public key
        self.public_key = public_key                     # public key
        self.__private_key = private_key                  # private key
    
    # Print the wallet (Only for testing purposes)   
    def __print_wallet(self):
        print("Wallet address:", self.lemonade_address)
        print("Wallet public key:", self.public_key)
        print("Wallet private key:", self.__private_key.export_key().decode('utf-8'))
        
    # Sign the data with the private key
    def sign(self, data: bytes) -> str:
        # Create a SHA-256 hash of the data
        data_hash = SHA256.new(data)
        # Sign the hash using the private key
        signature = pkcs1_15.new(self.__private_key).sign(data_hash)
        return binascii.hexlify(signature).decode("utf-8")