# wallet/utils.py:
import hashlib
from Crypto.PublicKey import RSA
from wallet.juiceWallet import JuiceWallet
import binascii

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
    private_key = RSA.generate(3072)
    public_key = private_key.publickey().export_key()
    public_key_hex = binascii.hexlify(public_key).decode('utf-8')
    hash1 = calculate_hash_sha256(public_key_hex)
    hash2 = calculate_hash_ripemd160(hash1)
    wallet_address = hash2
    return JuiceWallet(public_key_hex, private_key, wallet_address)
 
# Test the wallet
# wallet = initialize_wallet()