# This class is for network control on blockchain nodes.
# They have always a updated and persistent copy of the blockchain.
# They recieve transactions and validate them through the blockchain.
# Guarentee the consensus of the blockchain.

from blockchain.lemonBlock import LemonBlock
from blockchain.utils import *

from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

import copy
import json
import binascii

class NetworkNodeClient:
    def __init__(self, blockchain: LemonBlock) -> None:
        self.blockchain = blockchain # The blockchain of the node (last block)
        self.transaction_data = {}
        self.signature = ""
        self.inputs = ""
        self.outputs = ""
    
    # Receive a transaction for a node
    def receive(self, transaction: dict):
        self.transaction_data = transaction
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]
        
    # Validate the transaction
    def validade(self):
        self.validate_signature()
        self.validade_funds_are_owned_by_sender_and_input_equal_output()
    
    # make sure the transaction is valid
    # if it fails will throw an exception
    def validate_signature(self):
        transaction_data = copy.deepcopy(self.transaction_data)
        for count, tx_input in enumerate(transaction_data["inputs"]):
            tx_input_dict = json.loads(tx_input)
            public_key = tx_input_dict.pop("public_key")
            signature = tx_input_dict.pop("signature")
            transaction_data["inputs"][count] = json.dumps(tx_input_dict)
            signature_decoded = binascii.unhexlify(signature.encode("utf-8"))
            public_key_bytes = public_key.encode("utf-8")
            public_key_object = RSA.import_key(binascii.unhexlify(public_key_bytes))
            transaction_bytes = json.dumps(transaction_data, indent=2).encode('utf-8')
            transaction_hash = SHA256.new(transaction_bytes)
            # Try to verify the signature
            pkcs1_15.new(public_key_object).verify(transaction_hash, signature_decoded)
    
    # make sure the funds are valid and the sender has enough funds
    def validade_funds_are_owned_by_sender_and_input_equal_output(self):
        # Validade if the sender has enough funds  
        balance = 0
        pubkey_index = {}     
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            public_key = input_dict["public_key"]
            index = input_dict["output_index"]
            sender_address = calculate_hash_rimpemd160(calculate_hash(public_key))
            balance = get_balance_from_address(public_key=public_key,address=sender_address,blockchain=self.blockchain)
            # Store the index associated with the public key
            if public_key in pubkey_index:
                pubkey_index[public_key].append(index)
            else:
                pubkey_index[public_key] = [index]
        # Now for each index in output the sum of amounts is less or equal than the balance
        for public_key in pubkey_index:
            total_amount = 0
            for index in pubkey_index[public_key]:
                output_dict = json.loads(self.outputs[index])
                amount = output_dict["amount"]
                total_amount = total_amount + amount
            if total_amount > balance:
                raise TransactionException("TransactionException", "Sender does not have enough funds")
           
    
# Get balance from address
def get_balance_from_address(public_key:str, address: str, blockchain: LemonBlock) -> int:
    current_block = blockchain
    balance = 0
    out_lc = 0
    in_lc = 0
    
    c = 0
    # For each block on blockchain
    while current_block:
        transaction_data = current_block.transaction_data
        outputs = transaction_data["outputs"]
        inputs = transaction_data["inputs"]
        c = c + 1
        
        # For each output on transaction
        for output in outputs:
            output = json.loads(output)
            # If the address is the same as the address passed as parameter
            # Sum the amount to the out_lc
            if (output["public_key_hash"] == address):
                out_lc = int(output["amount"]) + out_lc

        # For each input on transaction
        for input in inputs:
            input = json.loads(input)
            # If the address is the same as the address passed as parameter
            # Sum the amount to the in_lc
            if (input["public_key"] == public_key):
                index = int(input["output_index"])
                output = outputs[index]
                output = json.loads(output)
                in_lc = int(output["amount"]) + in_lc
        # Get the previous block
        current_block = current_block.get_previous_block()
    # Calculate the balance
    balance = out_lc - in_lc
    return balance

# Exception for transaction
class TransactionException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message