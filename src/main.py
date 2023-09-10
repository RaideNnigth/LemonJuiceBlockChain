from flask import Flask, request

from blockchain.networkNodeClient import NetworkNodeClient, TransactionException
from initialize_blockchain import blockchain

app = Flask(__name__)

blockchain_base = blockchain()

@app.route("/transactions", methods=['POST'])
def validate_transaction():
    content = request.json
    try:
        node = NetworkNodeClient(blockchain_base)
        node.receive(transaction=content["transaction"])
        node.validade()
        node.validate_funds()
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "Transaction success", 200