import hashlib
def calculate_hash(data: str):
    return hashlib.sha256(data.encode()).hexdigest()