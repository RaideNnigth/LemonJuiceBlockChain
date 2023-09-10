# wallet/utils.py:
import hashlib
from Crypto.PublicKey import RSA
from wallet.juiceWallet import JuiceWallet
from blockchain.lemonBlock import LemonBlock
import binascii
import json

# Calculate the hash of a string using SHA256
# and return the hex representation of it
def calculate_hash_sha256(data: str):
    sha = hashlib.sha256()
    hash_str = data.encode('utf-8')
    sha.update(hash_str)
    return sha.hexdigest()

# Calculate the hash of a string using RIPEMD160
# and return the hex representation of it
def calculate_hash_ripemd160(data: str):
    ripemd = hashlib.new('ripemd160')
    hash_str = data.encode('utf-8')
    ripemd.update(hash_str)
    return ripemd.hexdigest()

# Initialize a wallet with a public key, private key and address
def initialize_wallet():
    private_key = RSA.generate(1024)
    public_key = private_key.publickey().export_key()
    public_key_hex = binascii.hexlify(public_key).decode('utf-8')
    hash1 = calculate_hash_sha256(public_key_hex)
    hash2 = calculate_hash_ripemd160(hash1)
    wallet_address = hash2
    return JuiceWallet(public_key_hex, private_key, wallet_address), binascii.hexlify(private_key.export_key())

# Get address from public key to lemonade wallet
def get_address_from_public_key(public_key_hex: str):
    hash1 = calculate_hash_sha256(public_key_hex)
    hash2 = calculate_hash_ripemd160(hash1)
    return hash2

# Import private key to RSA object
def import_private_key(private_key_hex: str):
    return RSA.import_key(binascii.unhexlify(private_key_hex))

# Validate pair key
def validate_pair_key(public_key_hex: str, private_key_hex: str):
    private_key_object = import_private_key(private_key_hex)
    public_key = private_key_object.publickey().export_key()
    public_key_hex2 = binascii.hexlify(public_key).decode('utf-8')
    if (public_key_hex == public_key_hex2):
        return True
    else:
        return False


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
        
        print(f"block: {c}")
        c = c + 1
        
        # For each output on transaction
        for output in outputs:
            output = json.loads(output)
            # If the address is the same as the address passed as parameter
            # Sum the amount to the out_lc
            if (output["public_key_hash"] == address):
                out_lc = int(output["amount"]) + out_lc
                print("Received: ", int(output["amount"]))

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
                print("Sent: ", int(output["amount"]))
        # Get the previous block
        current_block = current_block.get_previous_block()
    # Calculate the balance
    balance = out_lc - in_lc
    print("balance: ", balance)
    return balance

# Test the wallet
# wallet = initialize_wallet()
