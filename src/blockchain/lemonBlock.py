import json
from blockchain.utils import calculate_hash

class LemonBlock:
    # Constructor for the LemonBlock class
    def __init__(self, time_stamp, transaction_data: dict, previous_block=None):
        self.previous_block = previous_block
        self.transaction_data = transaction_data
        self.timestamp = time_stamp
    
    # Method to calculate the hash of the block
    def cryptografic_hash(self) -> str:
        block_content = {
            "transaction_data": self.transaction_data,
            "previous_block": self.previous_block.cryptografic_hash() if self.previous_block else None,
            "timestamp": self.timestamp
        }
        return calculate_hash(json.dumps(block_content, indent=None))
    
    def get_previous_block(self):
        return self.previous_block
    
    

"""
# Transactions testing data

# Dont forget that if you wanna test it here you would need to create a timestamp for each block
import datetime
timestamp = datetime.datetime.now().strftime("%m%d%Y%H%M%S")

t1 = "John sends 2 LC to Mike"
t2 = "Mike sends 2.5 LC to John"
t3 = "John sends 1 LC to Mike"
t4 = "Mike sends 0.5 LC to John"
t5 = "John sends 3 LC to Mike"
t6 = "Mike sends 1 LC to John"

# Initial block creation
initial_block = LemonBlock("Initial String", timestamp,[t1, t2])

# Print the hash of the initial block
print(initial_block.transaction_data)
print(initial_block.cryptografic_hash())

# Second block creation
second_block = LemonBlock(initial_block.cryptografic_hash(), timestamp,[t3, t4])

# Print the hash of the second block
print(second_block.transaction_data)
print(second_block.cryptografic_hash())

# Third block creation
third_block = LemonBlock(second_block.cryptografic_hash(), timestamp,[t5, t6])

# Print the hash of the third block
print(third_block.transaction_data)
print(third_block.cryptografic_hash())
"""