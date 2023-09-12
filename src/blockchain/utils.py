import hashlib

def calculate_hash(data: str):
    return hashlib.sha256(data.encode()).hexdigest()

def calculate_hash_rimpemd160(data: str):
    return hashlib.new("ripemd160", data.encode()).hexdigest()
