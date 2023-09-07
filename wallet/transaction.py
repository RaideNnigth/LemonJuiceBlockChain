# Transaction class
from juiceWallet import JuiceWallet
from transactionInput import TransactionInput
from transactionOutput import TransactionOutput

import utils
import json

class Transaction:
    def __init__(self, owner: JuiceWallet, inputs : list[TransactionInput], outputs: list[TransactionOutput]) -> None:
        self.owner = owner
        self.inputs = inputs
        self.outputs = outputs
        self.signature = owner.sign(self.generate_data())
    
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
    
# Test the transaction

wallet = utils.initialize_wallet()
receiver = utils.initialize_wallet()

#owner: JuiceWallet, receiver_lemoncoin_address: bytes, amount: int, signature: str = ""

#transaction = Transaction(wallet, receiver.lemonade_address, 10)
#print(transaction.signature)
#transaction_data = transaction.send_to_nodes()