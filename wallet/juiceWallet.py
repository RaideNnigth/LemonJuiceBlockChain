# Path: wallet/juiceWallet.py
# Wallet class for JuiceCoin

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from wallet.transaction import Transaction, TransactionInput, TransactionOutput

import requests

# JuiceWallet class
# This class represents a wallet with a public key, private key and address
# The amount is saved in the blockchain
# The address is the hash of the public key (publicKey->sha256->ripemd160 = address)
class JuiceWallet:
    def __init__(self, public_key_hex: str, private_key: RSA.RsaKey, address: str):
        self.lemonade_address = address                  # address is the hash of the public key
        self.public_key = public_key_hex                     # public key
        self.__private_key = private_key                  # private key
        self.node = Node()
    
    # Print the wallet (Only for testing purposes)   
    def __print_wallet(self):
        print("Wallet address:", self.lemonade_address)
        print("Wallet public key:", self.public_key)
        print("Wallet private key:", self.__private_key.export_key().decode('utf-8'))
    
    # Sign the data with the private key
    def sign(self, data: bytes) -> bytes:
        # Create a SHA-256 hash of the data
        data_hash = SHA256.new(data)
        # Sign the hash using the private key
        signature = pkcs1_15.new(self.__private_key).sign(data_hash)
        return signature
    
    # Process Transaction 
    def process_transaction(self, inputs: list[TransactionInput], outputs: list[TransactionOutput]) -> requests.Response:
        transaction = Transaction(self, inputs, outputs)
        transaction.sign()
        return self.node.send({"transaction": transaction.generate_data()})
    
class Node:
    def __init__(self):
        ip = "127.0.0.1"
        port = 5000
        self.base_url = f"http://{ip}:{port}/"

    def send(self, transaction_data: dict) -> requests.Response:
        url = f"{self.base_url}transactions"
        req_return = requests.post(url, json=transaction_data)
        req_return.raise_for_status()
        return req_return