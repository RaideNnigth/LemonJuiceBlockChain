# Transaction class
from juiceWallet import JuiceWallet
import utils

class Transaction:
    def __init__(self, owner: JuiceWallet, receiver_lemoncoin_address: str, amount: int):
        self.owner = owner
        self.receiver_lemoncoin_address = receiver_lemoncoin_address
        self.amount = amount
        self.signature = owner.sign(self.generate_data())
    
    # generate data for transaction
    def generate_data(self) -> bytes:
        transaction_data = utils.generate_transaction_data(self.owner.lemonade_address, self.receiver_lemoncoin_address, self.amount)
        return utils.convert_transaction_data_to_bytes(transaction_data)
    # Send to nodes in blockchain
    def send_to_nodes(self):
        return {
            "sender_address": self.owner.lemonade_address,
            "receiver_address": self.receiver_lemoncoin_address,
            "amount": self.amount,
            "signature": self.signature
        }
    
    
# Test the transaction

wallet = utils.initialize_wallet()
receiver = utils.initialize_wallet()

#owner: JuiceWallet, receiver_lemoncoin_address: bytes, amount: int, signature: str = ""
transaction = Transaction(wallet, receiver.lemonade_address, 10)
print(transaction.signature)
transaction_data = transaction.send_to_nodes()