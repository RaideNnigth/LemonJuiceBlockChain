# Transaction class
from wallet.juiceWallet import JuiceWallet
from wallet.transactionInput import TransactionInput
from wallet.transactionOutput import TransactionOutput

#import wallet.utils
import json
import binascii

class Transaction:
    def __init__(self, owner: JuiceWallet, inputs : list[TransactionInput], outputs: list[TransactionOutput]) -> None:
        self.owner = owner
        self.inputs = inputs
        self.outputs = outputs
        
    # generate data for transaction
    def generate_data(self) -> bytes:
        transaction_dict = {
            "inputs": [i.to_json(False) for i in self.inputs],
            "outputs": [o.to_json() for o in self.outputs]
        }
        transaction_bytes = json.dumps(transaction_dict).encode('utf-8')
        return transaction_bytes
        
    # Send to nodes in blockchain
    def send_to_nodes(self):
        return {
            "inputs": [i.to_json() for i in self.inputs],
            "outputs": [o.to_json() for o in self.outputs]
        }
            
    def sign_transaction_data(self) -> bytes:
        transaction_dict = {
            "inputs": [tx_input.to_json(with_signature_and_public_key=False) for tx_input in self.inputs],
            "outputs": [tx_output.to_json() for tx_output in self.outputs]
        }
        signature = self.owner.sign(json.dumps(transaction_dict, indent=2).encode('utf-8'))
        return signature
    
    
    def sign(self):
        signature_hex = binascii.hexlify(self.sign_transaction_data()).decode("utf-8")
        for transaction_input in self.inputs:
            transaction_input.signature = signature_hex
            transaction_input.public_key = self.owner.public_key
        
# Test the transaction

#wallet = utils.initialize_wallet()
#receiver = utils.initialize_wallet()

#owner: JuiceWallet, receiver_lemoncoin_address: bytes, amount: int, signature: str = ""

#transaction = Transaction(wallet, receiver.lemonade_address, 10)
#print(transaction.signature)
#transaction_data = transaction.send_to_nodes()