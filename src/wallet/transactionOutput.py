# This class will represente the outputs of the transaction

import json

class TransactionOutput:
    def __init__(self, public_key_hash: str, amount: int) -> None:
        self.public_key_hash = public_key_hash
        self.amount = amount
    
    def to_json(self) -> str:
        return json.dumps({
            "public_key_hash": self.public_key_hash,
            "amount": self.amount
        })