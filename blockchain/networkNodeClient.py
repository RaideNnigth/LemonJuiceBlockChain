# This class is for network control on blockchain nodes.
# They have always a updated and persistent copy of the blockchain.
# They recieve transactions and validate them through the blockchain.
# Guarentee the consensus of the blockchain.

from blockchain.lemonBlock import LemonBlock
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from blockchain.utils import *

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
        self.validade_funds_are_owned_by_sender()
        self.validate_funds()
    
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
    
    # just get all transactions from utxo
    def get_transaction_from_utxo(self, utxo_hash: str) -> dict:
        current_block = self.blockchain
        while current_block:
            if utxo_hash == current_block.cryptografic_hash():
                return current_block.transaction_data
            current_block = current_block.get_previous_block()
        return {}
    
    # make sure the funds are valid and the sender has enough funds
    def validade_funds_are_owned_by_sender(self):
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            public_key = input_dict["public_key"]
            sender_public_key_hash = calculate_hash_rimpemd160(calculate_hash(public_key))
            transaction_data = self.get_transaction_from_utxo(input_dict["transaction_hash"])
            public_key_hash = json.loads(transaction_data["outputs"][input_dict["output_index"]])["public_key_hash"]
            assert public_key_hash == sender_public_key_hash    
    
    # make sure the funds are valid
    def validate_funds(self):
        assert self.get_total_amount_in_inputs() == self.get_total_amount_in_outputs()
    
    # get the total amount of funds in the inputs
    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            transaction_data = self.get_transaction_from_utxo(input_dict["transaction_hash"])
            utxo_amount = json.loads(transaction_data["outputs"][input_dict["output_index"]])["amount"]
            total_in = total_in + utxo_amount
        return total_in

    # get the total amount of funds in the outputs
    def get_total_amount_in_outputs(self) -> int:
        total_out = 0
        for tx_output in self.outputs:
            output_dict = json.loads(tx_output)
            amount = output_dict["amount"]
            total_out = total_out + amount
        return total_out
    
    # Iterative way through the blockchain to get funds to a addres and validate it against amount
    def validate_funds_iterative(self, sender_address: str, amount: float) -> bool:
        # get the balance of the sender
        sender_balance = 0
        current_block = self.blockchain
        while current_block:
            if current_block.transaction_data["sender"] == sender_address:
                sender_balance = sender_balance - current_block.transaction_data["amount"]
            if current_block.transaction_data["receiver"] == sender_address:
                sender_balance = sender_balance + current_block.transaction_data["amount"]
            current_block = current_block.get_previous_block()
        if sender_balance < amount:
            return False
        return True
    