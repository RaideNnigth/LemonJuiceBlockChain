from flask import Flask, render_template, url_for, request

from blockchain.networkNodeClient import NetworkNodeClient, TransactionException
from blockchain.initialize_blockchain import blockchain

app = Flask(__name__)

blockchain_base = blockchain()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        return render_template(url_for('index'))
        
    else: 
        return render_template('home.html')

@app.route('/login', methods=['GET'])
def get_wallet_info():
    public_key = request.args.get('public_key')
    
    # TODO: get balance agains public key
    
    
    
    return "Login Success", 200



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


if __name__ == '__main__':
    app.run(debug=True)
