from flask import Flask, render_template, url_for, request

from blockchain.networkNodeClient import NetworkNodeClient, TransactionException
from blockchain.initialize_blockchain import blockchain

from wallet.juiceWallet import JuiceWallet
from wallet.utils import get_address_from_public_key, validate_pair_key, get_balance_from_address, import_private_key

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
    private_key = request.args.get('private_key')
    
    # Validade if public key and private key are not empty
    if (public_key is None or private_key is None):
        return "Login Failed, public key or private key empty", 400
    
    # Validade if public key and private key are a pair
    try:
        private_key_object = validate_pair_key(public_key, private_key)
    except:
        return "Login Failed, Keys does not match", 400
    
    # Import private key to RSA object
    private_key_object = import_private_key(private_key)
    
    # returns for the user the wallet address and balance, and wallet object
    wallet = JuiceWallet(public_key, private_key_object, get_address_from_public_key(public_key))
    balance = get_balance_from_address(wallet.lemonade_address, blockchain_base)
    address = wallet.lemonade_address
    
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
